import queue
import os
import logging
from flask import Blueprint, Response, current_app
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configure logging
log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=log_level, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


livereload_bp = Blueprint("livereload", __name__)

change_queue = queue.Queue()


class ChangeHandler(FileSystemEventHandler):
    def __init__(self, ignore_patterns=None):
        super().__init__()
        self.ignore_patterns = ignore_patterns or []

    def on_any_event(self, event):
        if self.should_ignore(event.src_path):
            return

        logger.debug(f"File changed: {event.src_path}")
        change_queue.put("reload")

    def should_ignore(self, path):
        for pattern in self.ignore_patterns:
            if pattern in path:
                logger.debug(f"Ignoring change in: {path}")
                return True
        return False


@livereload_bp.route("/_livereload")
def sse():
    def gen():
        while True:
            try:
                message = change_queue.get(timeout=10)
                yield f"data: {message}\n\n"
            except queue.Empty:
                pass

    return Response(gen(), mimetype="text/event-stream")


def start_watcher(app):
    observer = Observer()
    default_ignore_patterns = [
        "__pycache__",
        ".venv",
        ".git",
        ".pytest_cache",
    ]
    ignore_patterns = app.config.get('LIVERELOAD_IGNORE_PATTERNS') or default_ignore_patterns
    handler = ChangeHandler(ignore_patterns=ignore_patterns)

    # Watch app directory for .py file changes
    app_root = app.root_path
    observer.schedule(handler, app_root, recursive=True)

    # Watch templates and static folders
    template_folder = app.template_folder
    static_folder = app.static_folder
    if template_folder and os.path.exists(template_folder):
        observer.schedule(handler, template_folder, recursive=True)
    if static_folder and os.path.exists(static_folder):
        observer.schedule(handler, static_folder, recursive=True)

    if observer.emitters:
        observer.start()


def setup_watcher(setup_state):
    """Start the file watcher when the blueprint is registered."""
    app = setup_state.app
    if not app.debug or os.environ.get("WERKZEUG_RUN_MAIN") != "true":
        return
    start_watcher(app)


livereload_bp.record_once(setup_watcher)
