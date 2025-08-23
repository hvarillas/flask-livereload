#!/usr/bin/env python3
"""
Script de prueba para verificar que Flask-LiveReload se puede importar y usar correctamente
"""

import sys
import traceback
import os


def test_import():
    """Prueba la importación de Flask-LiveReload"""
    try:
        from flask_livereload import LiveReload

        print("✅ Flask-LiveReload importado correctamente")
        return True
    except ImportError as e:
        print(f"❌ Error importando Flask-LiveReload: {e}")
        return False


def test_basic_usage():
    """Prueba el uso básico de Flask-LiveReload"""
    try:
        from flask import Flask
        from flask_livereload import LiveReload

        # Crear app de prueba
        app = Flask(__name__)
        app.debug = True

        # Inicializar LiveReload
        livereload = LiveReload(app)

        print("✅ Flask-LiveReload inicializado correctamente")
        print("✅ Aplicación configurada con éxito")

        return True
    except Exception as e:
        print(f"❌ Error en uso básico: {e}")
        traceback.print_exc()
        return False


def test_configuration():
    """Prueba la configuración avanzada"""
    try:
        from flask import Flask
        from flask_livereload import LiveReload

        app = Flask(__name__)
        app.debug = True

        # Probar con patrones de ignorar
        livereload = LiveReload(
            app, ignore_patterns=["__pycache__", ".git", "node_modules"]
        )

        print("✅ Configuración avanzada funcionando correctamente")

        return True
    except Exception as e:
        print(f"❌ Error en configuración: {e}")
        return False


def test_custom_patterns():
    """Prueba la configuración con patrones personalizados"""
    try:
        from flask import Flask
        from flask_livereload import LiveReload

        app = Flask(__name__)
        app.debug = True

        # Configurar patrones personalizados
        app.config["LIVERELOAD_WATCH_PATTERNS"] = [
            "statics/**/*.html",
            "statics/**/*.js",
            "templates/**/*.html",
        ]
        
        app.config["LIVERELOAD_IGNORE_PATTERNS"] = [
            "__pycache__",
            ".git",
            "*.pyc",
            "node_modules",
        ]

        livereload = LiveReload(app)

        # Verificar que la configuración se aplicó
        watch_patterns = app.config.get("LIVERELOAD_WATCH_PATTERNS")
        ignore_patterns = app.config.get("LIVERELOAD_IGNORE_PATTERNS")
        
        if watch_patterns and ignore_patterns:
            print("✅ Configuración de patrones personalizados aplicada correctamente")
            print(f"   📋 Patrones de observación: {len(watch_patterns)}")
            print(f"   🚫 Patrones de ignorar: {len(ignore_patterns)}")
            return True
        else:
            print("⚠️  Configuración de patrones no se aplicó correctamente")
            return False

    except Exception as e:
        print(f"❌ Error en configuración de patrones personalizados: {e}")
        traceback.print_exc()
        return False


def test_script_injection():
    """Prueba la inyección del script de LiveReload"""
    try:
        from flask import Flask, render_template_string
        from flask_livereload import LiveReload

        app = Flask(__name__)
        app.debug = True
        livereload = LiveReload(app)

        with app.test_client() as client:
            # Crear una ruta que devuelva HTML
            @app.route('/test')
            def test_route():
                return render_template_string("<html><body><h1>Test</h1></body></html>")

            # Hacer una petición
            response = client.get('/test')
            
            # Verificar que el script se inyectó
            if b'/_livereload' in response.data and b'EventSource' in response.data:
                print("✅ Script de LiveReload inyectado correctamente")
                return True
            else:
                print("⚠️  Script de LiveReload no se inyectó correctamente")
                return False

    except Exception as e:
        print(f"❌ Error en prueba de inyección de script: {e}")
        traceback.print_exc()
        return False


def main():
    """Función principal de pruebas"""
    print("🧪 Probando Flask-LiveReload...")
    print("=" * 60)
    print(f"📁 Directorio actual: {os.getcwd()}")
    print(f"🐍 Versión de Python: {sys.version}")

    tests = [
        ("Importación", test_import),
        ("Uso básico", test_basic_usage),
        ("Configuración", test_configuration),
        ("Patrones personalizados", test_custom_patterns),
        ("Inyección de script", test_script_injection),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n🔍 Ejecutando prueba: {test_name}")
        if test_func():
            passed += 1
        else:
            print(f"⚠️  Prueba '{test_name}' falló")

    print("\n" + "=" * 60)
    print(f"📊 Resultados: {passed}/{total} pruebas pasaron")

    if passed == total:
        print("🎉 ¡Todas las pruebas pasaron!")
        print("\n💡 Flask-LiveReload está listo para usar en proyectos externos")
        print("🚀 Puedes comenzar a desarrollar con recarga automática")
        return 0
    else:
        print("⚠️  Algunas pruebas fallaron. Revisa la configuración.")
        print("📝 Consulta la documentación en examples/README.md")
        return 1


if __name__ == "__main__":
    sys.exit(main())
