"""
Flask-LiveReload
----------------

A Flask extension that provides live reloading of web pages when template or static files change.
"""
import os
from flask import Flask

class LiveReload:
    """
    This class is used to control the Flask-LiveReload extension.
    """
    def __init__(self, app: Flask = None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask):
        """
        Initializes the extension with the given application.
        """
        if not app.debug:
            return

        # More logic will be added here.
        app.extensions['livereload'] = self

        from .views import livereload_bp
        app.register_blueprint(livereload_bp)

        @app.after_request
        def inject_script(response):
            if response.content_type.startswith('text/html'):
                script = b'''
<script>
    var source = new EventSource("/_livereload");
    source.onmessage = function(event) {
        if (event.data == "reload") {
            window.location.reload();
        }
    };
</script>
'''
                response.data += script
            return response