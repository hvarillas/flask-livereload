from flask import Flask, render_template
from flask_autoreload import AutoReload

app = Flask(__name__)
app.debug = True
LiveReload(app)

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run()