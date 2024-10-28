# reconocimiento_music/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload, name='upload'),  # Ruta para la vista de carga
    # No es necesario tener la ruta de redirección aquí
    # La redirección se maneja en el archivo principal de URLs
]
