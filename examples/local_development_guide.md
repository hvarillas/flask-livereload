# 🔧 Guía de Desarrollo Local - Flask-LiveReload

Esta guía te explica cómo trabajar con Flask-LiveReload en modo desarrollo local, sin necesidad de subir cambios a Git.

## 📦 Instalación en Modo Desarrollo

### Instalación Inicial

```bash
# Navega al directorio del proyecto
cd /path/to/flask-livereload

# Instala en modo desarrollo
pip install -e .

# O si usas uv (recomendado por ser más rápido)
uv pip install -e .
```

**¿Qué hace `-e`?**
- Instala el paquete en modo "editable"
- Los cambios en el código se reflejan inmediatamente
- No necesitas reinstalar después de cada cambio
- Crea un enlace simbólico al código fuente

### Verificar Instalación

```bash
# Verifica que esté instalado
pip list | grep flask-livereload
# o
uv pip list | grep flask-livereload

# Deberías ver algo como:
# flask-livereload 0.1.0 (from file:///path/to/flask-livereload)
```

## 🔄 Actualizar Cambios Localmente

### Método 1: Reinstalación Forzada (Recomendado)

```bash
# Desde el directorio del proyecto
cd /path/to/flask-livereload

# Fuerza reinstalación manteniendo modo editable
pip install -e . --force-reinstall
# o
uv pip install -e . --force-reinstall
```

### Método 2: Solo si Cambias Dependencias

Si modificas `pyproject.toml` o `setup.py`:

```bash
# Actualiza las dependencias
pip install -e . --upgrade
# o
uv pip install -e . --upgrade
```

## 🧪 Probar Cambios Localmente

### Ejecutar Pruebas Automáticas

```bash
# Ejecutar pruebas unitarias
python -m pytest tests/

# Ejecutar script de verificación
python examples/test_import.py

# Ejecutar ejemplo personalizado
python examples/custom_watch_patterns_example.py
```

### Verificar Cambios en Tiempo Real

1. **Modifica el código** en `flask_livereload/src/flask_livereload/`
2. **Guarda los cambios**
3. **Reinicia** tu aplicación de prueba
4. **Verifica** que los cambios funcionen

## 🏗️ Flujo de Desarrollo Local

### 1. Configurar Entorno

```bash
# Clona o navega al repositorio
cd /path/to/flask-livereload

# Opcional: Crea entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows

# Instala en modo desarrollo
pip install -e .

# Instalar dependencias de desarrollo (si las hay)
pip install pytest watchdog
```

### 2. Hacer Cambios

```bash
# Edita los archivos fuente
vim flask_livereload/src/flask_livereload/__init__.py

# O usando VS Code
code flask_livereload/src/flask_livereload/__init__.py
```

### 3. Aplicar Cambios

```bash
# Para cambios en código Python (generalmente no necesario con -e)
pip install -e . --force-reinstall

# Para cambios en setup.py o pyproject.toml
pip install -e . --upgrade
```

### 4. Probar Cambios

```bash
# Ejecutar todas las pruebas
python -m pytest tests/ -v

# Ejecutar script de verificación
python examples/test_import.py

# Probar con ejemplo personalizado
python examples/custom_watch_patterns_example.py

# Probar con la demo principal
python main.py
```

## 🔍 Depuración de Problemas

### Error: "ImportError: cannot import name 'LiveReload'"

**Solución:**
```bash
# Reinstala el paquete
cd /path/to/flask-livereload
pip install -e . --force-reinstall

# Verifica instalación
python -c "from flask_livereload import LiveReload; print('✅ Import exitoso')"
```

### Error: "ModuleNotFoundError: No module named 'flask_livereload'"

**Solución:**
1. Verifica que estés en el directorio correcto
2. Reinstala: `pip install -e .`
3. Verifica: `pip list | grep flask-livereload`

### Los cambios no se reflejan

**Solución:**
1. **Verifica** que hayas instalado con `-e`
2. **Reinicia** tu aplicación Flask
3. **Verifica** que no haya errores de importación
4. **Revisa** los logs para errores

### Error de cache de Python

**Solución:**
```bash
# Limpia cache de Python
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true

# En Windows (PowerShell)
Get-ChildItem -Path . -Recurse -Name "__pycache__" | Remove-Item -Recurse -Force
Get-ChildItem -Path . -Recurse -Name "*.pyc" | Remove-Item -Force

# Reinicia aplicación
```

## 📁 Estructura de Desarrollo

```
flask-livereload/
├── flask_livereload/              # Paquete principal
│   ├── setup.py                  # Configuración setup.py (legacy)
│   └── src/
│       └── flask_livereload/     # Código fuente
│           ├── __init__.py      # Clase principal
│           └── views.py         # Blueprint SSE y manejadores
├── examples/                     # Ejemplos y pruebas
│   ├── README.md                # Documentación de ejemplos
│   ├── test_import.py           # Script de verificación
│   ├── standalone_example.py    # Ejemplo independiente
│   ├── custom_watch_patterns_example.py  # Ejemplo avanzado
│   └── local_development_guide.md       # Esta guía
├── tests/                        # Pruebas unitarias
│   └── test_livereload.py       # Pruebas principales
├── main.py                      # Demo del proyecto
├── pyproject.toml               # Configuración moderna del proyecto
├── README.md                    # Documentación principal
└── requirements.txt             # Dependencias (si existe)
```

## ⚡ Comandos Útiles

```bash
# Instalar en desarrollo
pip install -e .

# Actualizar cambios
pip install -e . --force-reinstall

# Verificar instalación
pip show flask-livereload

# Ejecutar todas las pruebas
python -m pytest tests/ -v

# Ejecutar scripts de prueba
python examples/test_import.py
python examples/custom_watch_patterns_example.py

# Limpiar cache de Python
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true

# Ver logs con nivel DEBUG
LOG_LEVEL=DEBUG python main.py
```

## 🧪 Desarrollo Guiado por Pruebas (TDD)

### 1. Escribir Prueba Primero

```python
# En tests/test_livereload.py
def test_custom_patterns():
    """Test custom watch patterns functionality"""
    # Tu nueva prueba aquí
```

### 2. Ejecutar Prueba (fallará)

```bash
python -m pytest tests/test_livereload.py::test_custom_patterns -v
```

### 3. Implementar Funcionalidad

Modificar `flask_livereload/src/flask_livereload/views.py`

### 4. Volver a Ejecutar Prueba

```bash
python -m pytest tests/test_livereload.py::test_custom_patterns -v
```

## 🔄 Workflow Recomendado

1. **Clona** el repositorio
2. **Instala** en modo desarrollo: `pip install -e .`
3. **Ejecuta** pruebas existentes: `python -m pytest tests/`
4. **Desarrolla** y haz cambios
5. **Escribe** nuevas pruebas si aplica
6. **Ejecuta** todas las pruebas: `python -m pytest tests/`
7. **Prueba** manualmente con ejemplos
8. **Documenta** cambios en README si aplica

## 🎯 Ventajas del Desarrollo Local

- ✅ **Cambios inmediatos**: No necesitas reinstalar para cada cambio (-e mode)
- ✅ **Debugging fácil**: Puedes usar debugger en tu IDE
- ✅ **Sin Git**: Trabajas localmente sin commits
- ✅ **Control total**: Modifica cualquier parte del código
- ✅ **Testing rápido**: Prueba cambios al instante
- ✅ **TDD**: Desarrollo guiado por pruebas

## 🛠️ Herramientas de Desarrollo Recomendadas

- **IDE**: VS Code con extensiones Python
- **Linting**: flake8, black
- **Testing**: pytest
- **Debugging**: Python debugger integrado en IDE
- **Versionado**: git (opcional para desarrollo local)

¿Necesitas ayuda con algún paso específico del desarrollo local?
