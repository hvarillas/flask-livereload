"""
Ejemplo de Flask-LiveReload con patrones de observación personalizados

Este ejemplo muestra cómo usar LIVERELOAD_WATCH_PATTERNS para especificar
exactamente qué archivos debe monitorear Flask-LiveReload.

## Características demostradas:

1. Patrones personalizados de observación
2. Patrones de ignorar extendidos
3. Múltiples tipos de archivos
4. Configuración avanzada
"""

import os
from flask import Flask, render_template, jsonify
from flask_livereload import LiveReload

app = Flask(__name__)
app.debug = True

# Configuración avanzada de patrones de observación personalizados
# Solo se recargará cuando cambien archivos que coincidan con estos patrones
app.config["LIVERELOAD_WATCH_PATTERNS"] = [
    # Archivos HTML en statics y subdirectorios
    "statics/**/*.html",
    "statics/**/*.htm",
    # Archivos JavaScript en statics y subdirectorios
    "statics/**/*.js",
    # Archivos CSS en statics y subdirectorios
    "statics/**/*.css",
    # Archivos de imagen
    "statics/**/*.png",
    "statics/**/*.jpg",
    "statics/**/*.jpeg",
    "statics/**/*.gif",
    "statics/**/*.svg",
    # Archivos de configuración específicos
    "config/*.json",
    "config/*.yaml",
    "config/*.yml",
    # Templates personalizados
    "templates/**/*.html",
    # Solo archivos Python específicos (modelos y servicios)
    "models/*.py",
    "services/*.py",
    "utils/*.py",
    # Archivos de datos
    "data/**/*.json",
    "data/**/*.csv",
    "data/**/*.xml",
]

# Patrones de ignorar extendidos para mejor rendimiento
app.config["LIVERELOAD_IGNORE_PATTERNS"] = [
    # Directorios de sistema y cache
    "__pycache__",
    ".venv",
    "venv",
    ".git",
    ".pytest_cache",
    ".vscode",
    ".idea",
    # Dependencias
    "node_modules",
    "bower_components",
    # Archivos compilados y temporales
    "*.pyc",
    "*.pyo",
    "*.pyd",
    "*.log",
    "*.tmp",
    "*.temp",
    "*.swp",
    "*.swo",
    # Archivos del sistema
    ".DS_Store",
    "Thumbs.db",
    ".directory",
    # Build y distribución
    "dist/",
    "build/",
    "*.egg-info/",
    ".eggs/",
    # IDE y editores
    "*.sublime-project",
    "*.sublime-workspace",
    ".vscode/",
    ".idea/",
]

# Inicializar Flask-LiveReload
livereload = LiveReload(app)


# Rutas de ejemplo
@app.route("/")
def index():
    """Página principal que usa una plantilla"""
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    """Dashboard que también usa plantillas"""
    return render_template("dashboard.html")


@app.route("/api/status")
def api_status():
    """Endpoint API que no debería provocar recarga"""
    return jsonify({
        "status": "ok", 
        "message": "API funcionando correctamente",
        "watching_patterns": len(app.config.get("LIVERELOAD_WATCH_PATTERNS", [])),
        "ignoring_patterns": len(app.config.get("LIVERELOAD_IGNORE_PATTERNS", []))
    })


@app.route("/test")
def test():
    """Página de prueba con información detallada"""
    patterns_info = "\n".join([f"  • {pattern}" for pattern in app.config["LIVERELOAD_WATCH_PATTERNS"][:10]])
    if len(app.config["LIVERELOAD_WATCH_PATTERNS"]) > 10:
        patterns_info += f"\n  ... y {len(app.config['LIVERELOAD_WATCH_PATTERNS']) - 10} más"

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test de Patrones Personalizados</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            .container {{ max-width: 800px; margin: 0 auto; }}
            .pattern-list {{ background: #f5f5f5; padding: 15px; border-radius: 5px; }}
            .info {{ background: #e3f2fd; padding: 15px; border-radius: 5px; margin: 20px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🧪 Test de Patrones Personalizados</h1>
            
            <div class="info">
                <h2>ℹ️ Cómo funciona:</h2>
                <p>Esta página se recargará <strong>solo</strong> si cambian archivos que coincidan 
                con los patrones configurados en <code>LIVERELOAD_WATCH_PATTERNS</code>.</p>
                
                <p>Por ejemplo:
                <ul>
                    <li>✅ Modificar un archivo <code>.js</code> en <code>statics/</code> provocará recarga</li>
                    <li>✅ Modificar un archivo <code>.html</code> en <code>templates/</code> provocará recarga</li>
                    <li>❌ Modificar un archivo <code>.py</code> en la raíz (excepto en <code>models/</code> o <code>services/</code>) NO provocará recarga</li>
                </ul>
                </p>
            </div>
            
            <div class="pattern-list">
                <h2>📋 Patrones de Observación Configurados ({len(app.config['LIVERELOAD_WATCH_PATTERNS'])} patrones):</h2>
                <pre>{patterns_info}</pre>
            </div>
            
            <div style="margin-top: 30px;">
                <h2>🧪 Pruebas Recomendadas:</h2>
                <ol>
                    <li>Modifica <code>statics/js/app.js</code> - Debería recargar</li>
                    <li>Modifica <code>templates/index.html</code> - Debería recargar</li>
                    <li>Modifica <code>models/user.py</code> - Debería recargar</li>
                    <li>Modifica <code>main.py</code> - NO debería recargar</li>
                    <li>Modifica <code>README.md</code> - NO debería recargar</li>
                </ol>
            </div>
        </div>
    </body>
    </html>
    """


if __name__ == "__main__":
    print("=" * 80)
    print("🚀 Flask-LiveReload con Patrones Personalizados - DEMO AVANZADA")
    print("=" * 80)
    print(f"📁 Directorio de trabajo: {os.getcwd()}")
    print(f"🔧 Modo debug: {app.debug}")
    print(f"📊 Patrones de observación: {len(app.config['LIVERELOAD_WATCH_PATTERNS'])}")
    print(f"🚫 Patrones de ignorar: {len(app.config['LIVERELOAD_IGNORE_PATTERNS'])}")
    print("\n🎯 Patrones clave configurados:")
    key_patterns = [
        "statics/**/*.js",
        "statics/**/*.html", 
        "templates/**/*.html",
        "models/*.py"
    ]
    for pattern in key_patterns:
        print(f"  • {pattern}")
    
    print("\n🔗 Accede a http://127.0.0.1:5000/test para probar")
    print("💡 Usa la página de test para ver qué cambios provocan recarga")
    print("=" * 80)

    app.run(debug=True, host="0.0.0.0", port=5000)
