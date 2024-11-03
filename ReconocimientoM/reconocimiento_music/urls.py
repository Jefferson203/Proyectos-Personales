# reconocimiento_music/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload, name='upload'),  # Ruta para la vista de carga
    path('clear_media/', views.clear_media_folder, name='clear_media'),  # Ruta para limpiar media
]
