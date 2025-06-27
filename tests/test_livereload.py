import os
import time
import pytest
from flask import Flask
from flask_livereload import LiveReload

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.debug = True
    LiveReload(app)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_script_injection(client):
    """Test that the livereload script is injected into HTML responses."""
    @client.application.route('/')
    def index():
        return "<html><body>Hello</body></html>"

    response = client.get('/')
    assert response.status_code == 200
    assert b'/_livereload' in response.data

def test_sse_mimetype(client):
    """Test that the SSE endpoint has the correct mimetype."""
    response = client.get('/_livereload')
    assert response.mimetype == 'text/event-stream'

def test_reload_on_template_change(client):
    """Test that a reload message is sent when a template file changes."""
    template_dir = client.application.template_folder
    os.makedirs(template_dir, exist_ok=True)
    template_path = os.path.join(template_dir, 'test.html')

    with client.get('/_livereload') as response:
        # Modify the template file
        with open(template_path, 'w') as f:
            f.write('test')
        time.sleep(1) # Give watchdog time to detect the change

        # Check for the reload message
        assert b'data: reload' in response.data

    os.remove(template_path)