# mi_proyecto/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView  # Importa RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='reconocimiento/', permanent=False)),  # Redirige a /reconocimiento/
    path('reconocimiento/', include('reconocimiento_music.urls')),  # Ruta para la app
]

# Configuración para servir archivos de medios en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
