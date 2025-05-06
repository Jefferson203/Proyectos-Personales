# views.py
import base64
import hashlib
import hmac
import os
import time
import json
import requests
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from moviepy.editor import VideoFileClip
from django.http import JsonResponse
import shutil


# Definir extensiones de video válidas como constante
VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mov', '.mkv']


# Función para generar la firma para ACRCloud
def generate_signature(access_secret, string_to_sign):
    return base64.b64encode(hmac.new(access_secret.encode('ascii'), string_to_sign.encode('ascii'),
                                     digestmod=hashlib.sha1).digest()).decode('ascii')

# Función para identificar una canción con ACRCloud
def identify_song_acrcloud(file_path):
    access_key = settings.ACR_ACCESS_KEY
    access_secret = settings.ACR_SECRET_KEY
    if access_key is None or access_secret is None:
        return "Error: Claves de acceso de ACRCloud no están configuradas correctamente."

    requrl = "http://identify-us-west-2.acrcloud.com/v1/identify"

    # Crear la firma para autenticación
    http_method = "POST"
    http_uri = "/v1/identify"
    data_type = "audio"
    signature_version = "1"
    timestamp = time.time()

    string_to_sign = "\n".join([http_method, http_uri, access_key, data_type, signature_version, str(timestamp)])
    sign = generate_signature(access_secret, string_to_sign)

    # Leer el archivo de audio
    if not os.path.exists(file_path):
        return "Error: archivo de audio no encontrado."

    sample_bytes = os.path.getsize(file_path)

    # Preparar la solicitud a ACRCloud
    files = [
        ('sample', ('audio.mp3', open(file_path, 'rb'), 'audio/mpeg'))
    ]
    data = {
        'access_key': access_key,
        'sample_bytes': sample_bytes,
        'timestamp': str(timestamp),
        'signature': sign,
        'data_type': data_type,
        "signature_version": signature_version
    }

    response = requests.post(requrl, files=files, data=data)
    if response.status_code == 200:
        response_data = response.json()
        if "status" in response_data and response_data["status"]["msg"] == "Success":
            return response_data["metadata"]["music"]
        else:
            return f"Error en reconocimiento: {response_data['status']['msg']}"
    else:
        return f"Error HTTP {response.status_code}: no se pudo conectar con ACRCloud."

# Extraer el audio si el archivo es un video
def extract_audio_from_video(video_path):
    audio_path = os.path.join(settings.MEDIA_ROOT, "temp_audio.mp3")
    with VideoFileClip(video_path) as video:
        video.audio.write_audiofile(audio_path)
    return audio_path

# Vista para subir el archivo y realizar el reconocimiento
def upload(request):
    if request.method == 'POST' and request.FILES.get('audio_file'):
        audio_file = request.FILES['audio_file']
        fs = FileSystemStorage()
        file_path = fs.save(audio_file.name, audio_file)
        file_path = os.path.join(settings.MEDIA_ROOT, file_path)

        # Determina si es un video y extrae el audio si es necesario
        _, file_extension = os.path.splitext(file_path)
        if file_extension.lower() in VIDEO_EXTENSIONS:
            audio_file_path = extract_audio_from_video(file_path)
        else:
            audio_file_path = file_path

        # Llamada a la función de reconocimiento
        song_info = identify_song_acrcloud(audio_file_path)

        # Limpia el archivo temporal de audio si se generó
        if audio_file_path and audio_file_path != file_path:
            try:
                os.remove(audio_file_path)
            except OSError as e:
                print(f"Error al eliminar archivo temporal: {e}")

        return render(request, 'reconocimiento_music/upload.html', {'song_info': song_info})
    
    return render(request, 'reconocimiento_music/upload.html')




# Vista para limpiar la carpeta de medios
def clear_media_folder(request):
    if request.method == 'POST':
        media_folder = settings.MEDIA_ROOT
        try:
            # Borra todos los archivos dentro de la carpeta "media"
            for filename in os.listdir(media_folder):
                file_path = os.path.join(media_folder, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            return JsonResponse({'status': 'success', 'message': 'Carpeta media limpiada exitosamente.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)
