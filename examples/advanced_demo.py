"""
Ejemplo avanzado de Flask-LiveReload con todas las mejoras implementadas

Este ejemplo muestra:
1. Configuración avanzada de patrones
2. Manejo de errores mejorado
3. Logging detallado
4. Uso de variables de entorno
"""

import os
import logging
from flask import Flask, render_template_string
from flask_livereload import LiveReload


# Configurar logging detallado
logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def create_app():
    """Crear aplicación Flask con configuración avanzada"""
    app = Flask(__name__)
    app.debug = True  # ⚠️ IMPORTANTE: Solo funciona en modo debug
    
    # Configuración avanzada de Flask-LiveReload
    app.config.update({
        # Patrones de archivos a observar
        "LIVERELOAD_WATCH_PATTERNS": [
            "statics/**/*.html",
            "statics/**/*.js", 
            "statics/**/*.css",
            "statics/**/*.png",
            "statics/**/*.jpg",
            "templates/**/*.html",
            "config/*.json",
            "models/*.py",
        ],
        
        # Patrones de archivos a ignorar
        "LIVERELOAD_IGNORE_PATTERNS": [
            "__pycache__",
            ".venv",
            "venv",
            ".git",
            ".pytest_cache",
            "*.pyc",
            "*.pyo",
            "*.log",
            ".DS_Store",
            "node_modules",
            "dist/",
            "build/",
        ]
    })
    
    # Inicializar Flask-LiveReload
    livereload = LiveReload(app)
    
    return app


def add_routes(app):
    """Agregar rutas a la aplicación"""
    
    @app.route("/")
    def index():
        return render_template_string("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Flask-LiveReload Demo Avanzada</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
                .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                h1 { color: #333; }
                .feature { background: #e3f2fd; padding: 15px; margin: 15px 0; border-radius: 5px; }
                .config { background: #f1f8e9; padding: 15px; margin: 15px 0; border-radius: 5px; }
                pre { background: #2d2d2d; color: #f8f8f2; padding: 15px; border-radius: 5px; overflow-x: auto; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚀 Flask-LiveReload Demo Avanzada</h1>
                
                <div class="feature">
                    <h2>🌟 Características Demostradas</h2>
                    <ul>
                        <li>✅ Recarga automática inteligente</li>
                        <li>✅ Patrones personalizados de observación</li>
                        <li>✅ Filtros avanzados de ignorar</li>
                        <li>✅ Manejo de errores mejorado</li>
                        <li>✅ Logging detallado</li>
                    </ul>
                </div>
                
                <div class="config">
                    <h2>⚙️ Configuración Actual</h2>
                    <p><strong>Modo Debug:</strong> {{ debug_mode }}</p>
                    <p><strong>Patrones de Observación:</strong> {{ watch_patterns|length }}</p>
                    <p><strong>Patrones de Ignorar:</strong> {{ ignore_patterns|length }}</p>
                </div>
                
                <h2>📋 Instrucciones de Prueba</h2>
                <ol>
                    <li>Modifica <code>statics/js/app.js</code> - Debería recargar</li>
                    <li>Modifica <code>templates/index.html</code> - Debería recargar</li>
                    <li>Modifica <code>models/user.py</code> - Debería recargar</li>
                    <li>Modifica <code>README.md</code> - NO debería recargar</li>
                    <li>Modifica <code>main.py</code> - NO debería recargar</li>
                </ol>
                
                <h2>🔧 Variables de Entorno</h2>
                <p>Para debugging detallado:</p>
                <pre>export LOG_LEVEL=DEBUG
python {{ script_name }}</pre>
                
                <div style="margin-top: 30px; text-align: center;">
                    <p><em>La página se recargará automáticamente cuando cambien archivos que coincidan con los patrones configurados.</em></p>
                </div>
            </div>
        </body>
        </html>
        """, 
        debug_mode=app.debug,
        watch_patterns=app.config.get("LIVERELOAD_WATCH_PATTERNS", []),
        ignore_patterns=app.config.get("LIVERELOAD_IGNORE_PATTERNS", []),
        script_name=os.path.basename(__file__)
        )
    
    @app.route("/about")
    def about():
        return render_template_string("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Acerca de - Flask-LiveReload</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
                .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>ℹ️ Acerca de Flask-LiveReload</h1>
                <p>Esta es una página de ejemplo para demostrar Flask-LiveReload.</p>
                <p>Modifica este archivo y la página se recargará automáticamente.</p>
                <a href="/">← Volver al inicio</a>
            </div>
        </body>
        </html>
        """)
    
    return app


def main():
    """Función principal"""
    print("=" * 70)
    print("🚀 FLASK-LIVERELOAD DEMO AVANZADA")
    print("=" * 70)
    print(f"📁 Directorio actual: {os.getcwd()}")
    print(f"🔧 Modo debug: True (requerido para LiveReload)")
    print(f"📋 Nivel de logging: {os.environ.get('LOG_LEVEL', 'INFO')}")
    
    # Crear aplicación
    app = create_app()
    
    # Agregar rutas
    add_routes(app)
    
    # Mostrar configuración
    watch_patterns = app.config.get("LIVERELOAD_WATCH_PATTERNS", [])
    ignore_patterns = app.config.get("LIVERELOAD_IGNORE_PATTERNS", [])
    
    print(f"\n🎯 Patrones de observación ({len(watch_patterns)}):")
    for pattern in watch_patterns[:5]:  # Mostrar solo los primeros 5
        print(f"  • {pattern}")
    if len(watch_patterns) > 5:
        print(f"  ... y {len(watch_patterns) - 5} más")
    
    print(f"\n🚫 Patrones de ignorar ({len(ignore_patterns)}):")
    for pattern in ignore_patterns[:5]:  # Mostrar solo los primeros 5
        print(f"  • {pattern}")
    if len(ignore_patterns) > 5:
        print(f"  ... y {len(ignore_patterns) - 5} más")
    
    print(f"\n🔗 Accede a http://127.0.0.1:5000")
    print("💡 Modifica archivos que coincidan con los patrones para ver la recarga automática")
    print("=" * 70)
    
    # Ejecutar aplicación
    app.run(debug=True, host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()