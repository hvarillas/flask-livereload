import queue
import os
from flask import Blueprint, Response, current_app
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

livereload_bp = Blueprint('livereload', __name__)

change_queue = queue.Queue()

class ChangeHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        change_queue.put("reload")

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
    handler = ChangeHandler()
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