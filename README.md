# Flask-LiveReload

Una extensión de Flask que proporciona recarga en vivo de las páginas web cuando los archivos de plantilla o estáticos cambian. Ideal para acelerar el desarrollo al eliminar la necesidad de recargar manualmente el navegador después de cada cambio.

## Características

- **Recarga automática**: Monitorea los directorios `templates` y `static` en busca de cambios en los archivos.
- **Integración sencilla**: Se integra fácilmente en cualquier aplicación Flask.
- **Ligera**: No tiene dependencias externas pesadas.
- **Eficiente**: Utiliza Server-Sent Events (SSE) para notificar al navegador de los cambios.

## Instalación

Dado que este es un repositorio privado, necesitarás un Token de Acceso Personal (Personal Access Token - PAT) de GitHub para instalar el paquete. Asegúrate de que el token tenga el permiso `repo`.

Una vez que tengas tu token, puedes instalar el paquete de la siguiente manera:

```bash
pip install git+https://<TU_TOKEN>@github.com/hvarillas/flask-livereload.git
```

**Recomendación:**

Para evitar exponer tu token, guárdalo en una variable de entorno y úsala durante la instalación:

```bash
export GITHUB_TOKEN="tu_token_aqui"
pip install git+https://${GITHUB_TOKEN}@github.com/hvarillas/flask-livereload.git
```

## Uso

Para empezar a usar Flask-LiveReload, simplemente importa la clase `LiveReload` y pásale tu aplicación Flask.

```python
from flask import Flask, render_template
from flask_livereload import LiveReload

app = Flask(__name__)
livereload = LiveReload(app)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
```

Ahora, cuando ejecutes tu aplicación en modo de depuración (`debug=True`), cualquier cambio que hagas en tus plantillas o archivos estáticos hará que el navegador se recargue automáticamente.

## ¿Cómo funciona?

Flask-LiveReload inyecta un pequeño script de JavaScript en tus páginas HTML. Este script se conecta a un endpoint de Server-Sent Events (SSE) en `/_livereload`. En el lado del servidor, un observador de archivos monitorea los directorios de plantillas y estáticos. Cuando se detecta un cambio, se envía un mensaje al navegador a través del SSE, lo que provoca que la página se recargue.

## Contribuciones

Las contribuciones son bienvenidas. Si tienes alguna idea, sugerencia o informe de error, por favor abre un issue o envía un pull request.

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.
