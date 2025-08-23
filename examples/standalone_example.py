"""
Ejemplo completo de uso de Flask-LiveReload en un proyecto independiente

Para usar Flask-LiveReload en otro proyecto:

1. Instalar el paquete desde GitHub:
   pip install git+https://<TU_TOKEN>@github.com/hvarillas/flask-livereload.git

2. O si tienes el repositorio localmente, instalar en modo desarrollo:
   pip install -e /path/to/flask-livereload

3. Usar en tu aplicación Flask como se muestra abajo
"""

from flask import Flask, render_template
from flask_livereload import LiveReload

# Crear aplicación Flask
app = Flask(__name__)
app.debug = True  # IMPORTANTE: Solo funciona en modo debug

# Inicializar Flask-LiveReload
# Opción 1: Inicialización simple
livereload = LiveReload(app)

# Opción 2: Con patrones de ignorar personalizados
# livereload = LiveReload(app, ignore_patterns=['node_modules', '.git', '__pycache__'])


# Rutas de ejemplo
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
