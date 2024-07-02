# scan documentos

## Inicio

> python -m django startproject scan_documentos

> python manage.py startapp AppScan

> python manage.py migrate

> En la carpeta del proyecto, vamos al archivo **settings.py** para agregar la aplicacion en **INSTALLED_APPS**

> Luego, para corroborar que las aplicaciones se crearon correctamante, ejecutamos :

python manage.py check AppScan

## Servidor:

Corremos el servidor para corroborar que funciona

> python manage.py runserver

En el archivo **settings.py** importamos

> import os from django.conf import settings

Para manejar los templates (en el caso que lleven) sin poner las rutar absolutas, configurándolo de esta manera:

```
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(settings.BASE_DIR, "Appcoder", "template")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
```

## Proyecto

- En la carpeta de las aplicaciones creamos el archivo urls.py para manejar el routing que utilizaremos en las mismas
  Para que lo anterior quede bien configurado, debemos configurar en el archivo urls.py del proyecto (entrega_final), quedando éste, de esta manera:

from django.contrib import admin
from django.urls import path, include
from AppScan import views

urlpatterns = [
path("admin/", admin.site.urls),
path("/", include("AppScan.urls")),
]
python -m pip install --upgrade pip setuptools


pip install pdfplumber
pip install traits


python -m venv myenv
source myenv/bin/activate  # En Windows: myenv\Scripts\activate
pip install -r requirements.txt

