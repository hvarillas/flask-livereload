# 🚀 Guía Completa para usar Flask-LiveReload

Esta guía te explica cómo integrar Flask-LiveReload en cualquier proyecto Flask, con ejemplos prácticos y mejores prácticas.

## 📦 Instalación

### Opción 1: Instalación desde GitHub (Recomendado para usuarios finales)

```bash
# Reemplaza <TU_TOKEN> con tu Personal Access Token de GitHub
pip install git+https://<TU_TOKEN>@github.com/hvarillas/flask-livereload.git
```

### Opción 2: Instalación desde repositorio local (Para desarrollo)

```bash
# Navegar al directorio del proyecto flask-livereload
cd /path/to/flask-livereload

# Instalar en modo desarrollo
pip install -e .
```

## 🔧 Configuración Básica

### 1. Configuración Mínima

```python
from flask import Flask, render_template
from flask_livereload import LiveReload

app = Flask(__name__)
app.debug = True  # ⚠️ IMPORTANTE: Solo funciona en modo debug

# Inicialización simple
livereload = LiveReload(app)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
```

### 2. Configuración Avanzada con Patrones Personalizados

```python
from flask import Flask, render_template
from flask_livereload import LiveReload

app = Flask(__name__)
app.debug = True

# Configurar patrones personalizados de observación
app.config["LIVERELOAD_WATCH_PATTERNS"] = [
    "statics/**/*.html",    # Todos los HTML en statics y subdirectorios
    "statics/**/*.js",      # Todos los JS en statics y subdirectorios
    "statics/**/*.css",     # Todos los CSS en statics y subdirectorios
    "templates/**/*.html",  # Todos los HTML en templates y subdirectorios
]

# Configurar patrones de ignorar
app.config["LIVERELOAD_IGNORE_PATTERNS"] = [
    "__pycache__",
    ".venv",
    ".git",
    ".pytest_cache",
    "*.pyc",
    "*.pyo",
    "*.log",
    ".DS_Store",
    "node_modules",
]

livereload = LiveReload(app)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
```

### 3. Inicialización Diferida (Factory Pattern)

```python
from flask import Flask
from flask_livereload import LiveReload

# Crear extensión sin aplicación
livereload = LiveReload()

def create_app():
    app = Flask(__name__)
    app.debug = True

    # Inicializar extensión con la aplicación
    livereload.init_app(app)

    return app

# Uso
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
```

## 🏗️ Estructura de Proyecto Recomendada

```
mi_proyecto/
├── app.py                    # Archivo principal
├── requirements.txt          # Dependencias
├── templates/               # Plantillas Jinja2
│   ├── index.html
│   ├── about.html
│   └── layout.html
├── static/                  # Archivos estáticos
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── app.js
│   └── images/
├── config/                  # Archivos de configuración (opcional)
│   └── settings.json
└── venv/                    # Entorno virtual (opcional)
```

## 📋 Ejemplos Completos

### Ejemplo 1: Aplicación Simple con Configuración Avanzada

```python
# app.py
from flask import Flask, render_template
from flask_livereload import LiveReload
import os

app = Flask(__name__)
app.debug = True

# Configuración avanzada
app.config.update(
    LIVERELOAD_WATCH_PATTERNS=[
        "static/**/*.html",
        "static/**/*.js",
        "static/**/*.css",
        "templates/**/*.html",
    ],
    LIVERELOAD_IGNORE_PATTERNS=[
        "__pycache__",
        ".venv",
        ".git",
        "*.pyc",
        "node_modules",
    ]
)

livereload = LiveReload(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    print("🚀 Flask-LiveReload Demo App")
    print("📁 Directorio actual:", os.getcwd())
    print("🔧 Modo debug:", app.debug)
    app.run(debug=True, host="0.0.0.0", port=5000)
```

### Ejemplo 2: Con Blueprints y Configuración Personalizada

```python
# app.py
from flask import Flask
from flask_livereload import LiveReload

def create_app():
    app = Flask(__name__)
    app.debug = True
    
    # Configuración personalizada
    app.config["LIVERELOAD_WATCH_PATTERNS"] = [
        "statics/**/*.js",
        "templates/**/*.html",
    ]
    
    # Inicializar extensión
    livereload = LiveReload(app)
    
    # Registrar blueprints
    from routes.main import main_bp
    app.register_blueprint(main_bp)
    
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
```

```python
# routes/main.py
from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def index():
    return render_template("index.html")

@main_bp.route("/about")
def about():
    return render_template("about.html")
```

## 🔍 Verificación de Funcionamiento

### 1. Ejecutar la aplicación

```bash
python app.py
```

Deberías ver en la consola:
```
INFO - Flask-LiveReload initialized successfully
INFO - Flask-LiveReload starting with watch patterns: ['statics/**/*.html', 'statics/**/*.js', 'statics/**/*.css', 'templates/**/*.html']
INFO - Flask-LiveReload watcher started with 3 watchers
* Running on http://127.0.0.1:5000
* Debug mode: on
```

### 2. Verificar en el navegador

1. Abre http://127.0.0.1:5000
2. Abre las herramientas de desarrollo (F12)
3. Ve a la pestaña "Network" o "Red"
4. Deberías ver una conexión SSE a `/_livereload`
5. En la consola, deberías ver: "LiveReload: Connected to server"

### 3. Probar la recarga automática

1. Modifica cualquier archivo en `templates/` o `static/`
2. Guarda el archivo
3. La página debería recargarse automáticamente
4. En la consola verás: "LiveReload: Reloading page..."

## ⚙️ Configuración Avanzada

### Variables de Entorno

```bash
# Configurar nivel de logging
export LOG_LEVEL=DEBUG

# Ejecutar aplicación
python app.py
```

### Configuración de Flask

```python
app.config.update(
    LIVERELOAD_WATCH_PATTERNS=[
        "statics/**/*.html",
        "statics/**/*.js",
        "statics/**/*.css",
        "templates/**/*.html",
        "config/*.json",        # Archivos de configuración
        "models/*.py",          # Modelos específicos
    ],
    LIVERELOAD_IGNORE_PATTERNS=[
        "__pycache__",
        ".venv",
        ".git",
        ".pytest_cache",
        "*.pyc",
        "*.pyo",
        "*.log",
        ".DS_Store",
        "node_modules",
        "dist/",                # Directorios de build
        "build/",
    ]
)
```

## 🎯 Patrones de Archivos

Flask-LiveReload soporta patrones glob para especificar qué archivos observar:

- `*.html` - Todos los archivos HTML
- `statics/**/*.js` - Todos los archivos JS en statics y subdirectorios
- `templates/*.html` - Archivos HTML solo en el directorio templates
- `config/*.json` - Archivos JSON en config

## 🐛 Solución de Problemas

### Error: "cannot import name 'LiveReload' from 'flask_livereload'"

**Solución:** Asegúrate de haber instalado el paquete correctamente
```bash
pip install git+https://<TU_TOKEN>@github.com/hvarillas/flask-livereload.git
```

### Error: "LiveReload disabled: app not in debug mode"

**Solución:** Activa el modo debug
```python
app.debug = True
# O al ejecutar:
# app.run(debug=True)
```

### No se recarga automáticamente

**Solución:**
1. Verifica que la aplicación esté en modo debug
2. Revisa que no haya errores de JavaScript en la consola
3. Verifica que los archivos estén en los directorios configurados
4. Revisa los logs para mensajes de error
5. Asegúrate de que los patrones de observación sean correctos

### Problemas con patrones personalizados

**Solución:**
1. Usa rutas relativas al directorio de la aplicación
2. Incluye `./` al inicio de los patrones si es necesario
3. Verifica que los patrones usen sintaxis glob correcta

### Logs no aparecen

**Solución:** Configura el logging
```bash
export LOG_LEVEL=DEBUG
```

## 📝 Mejores Prácticas

1. **Siempre usa `app.debug = True`** para desarrollo
2. **Configura patrones de ignorar** para archivos innecesarios
3. **Usa logging detallado** durante el desarrollo
4. **Prueba en diferentes navegadores**
5. **Verifica la consola** para errores de JavaScript
6. **Usa patrones específicos** en lugar de observar todo
7. **Incluye patrones de ignorar** comunes como `__pycache__`, `*.pyc`, etc.

## 🔧 Desarrollo Local

Para desarrollar y probar cambios en Flask-LiveReload:

```bash
# En el directorio del proyecto
pip install -e . --force-reinstall

# Probar con el script de ejemplo
python examples/test_import.py
```

## 🔗 Enlaces Útiles

- [Repositorio GitHub](https://github.com/hvarillas/flask-livereload)
- [Documentación Flask](https://flask.palletsprojects.com/)
- [Server-Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)
- [Patrones Glob](https://en.wikipedia.org/wiki/Glob_(programming))
