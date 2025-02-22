TurtleGlide
================

Introducción
------------

TurtleGlide es una herramienta para crear archivos dentro de la carpeta templates o static de una app de Django.

Instalación
------------

Instalar TurtleGlide en tu proyecto Django:

```bash
pip install TurtleGlide
```

Luego la instalas como una app de Django en INSTALLED_APPS:

```python
INSTALLED_APPS = [
    'TurtleGlide'
]
```

ahora llamamos al archivo setup.sh que estalara todas las dependencias necesarias
```bash
./setup.sh
```

uso de TurtleGlide
------------

hay tres paramentros obligatorios para el uso del comando creeate_archive:

- app_name: Nombre de la app
- file_path: Ruta del componente HTML
- --type: de forma determinada el tipo de archivo a crear: "template" para archivos en la carpeta templates, "static" para archivos en la carpeta static

comando de ejemplo:
------------

```bash
python manage.py create_archive "app_name" "file_path" --type="template"
```
