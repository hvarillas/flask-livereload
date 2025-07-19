import queue
import os
from flask import Blueprint, Response, current_app
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

livereload_bp = Blueprint('livereload', __name__)

change_queue = queue.Queue()

class ChangeHandler(FileSystemEventHandler):
    def __init__(self, ignore_patterns=None):
        super().__init__()
        self.ignore_patterns = ignore_patterns or []

    def on_any_event(self, event):
        if self.should_ignore(event.src_path):
            return
        change_queue.put("reload")

    def should_ignore(self, path):
        for pattern in self.ignore_patterns:
            if pattern in path:
                return True
        return False

@livereload_bp.route('/_livereload')
def sse():
    def gen():
        while True:
            try:
                message = change_queue.get(timeout=10)
                yield f"data: {message}\n\n"
            except queue.Empty:
                pass
    return Response(gen(), mimetype='text/event-stream')

def start_watcher(app):
    observer = Observer()
    ignore_patterns = [
        "__pycache__",
        ".venv",
        ".git",
        ".pytest_cache",
    ]
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

observer_started = False

@livereload_bp.before_app_request
def before_request():
    global observer_started
    if not observer_started:
        start_watcher(current_app)
        observer_started = True