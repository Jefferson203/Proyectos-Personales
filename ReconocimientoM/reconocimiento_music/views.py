import os, re
import requests
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from moviepy.editor import VideoFileClip
from django.shortcuts import redirect

def extract_audio_from_video(video_path):
    audio_path = os.path.join(settings.MEDIA_ROOT, "temp_audio.mp3")
    
    with VideoFileClip(video_path) as video:
        video.audio.write_audiofile(audio_path)
    return audio_path

def identify_song(file_path, api_token):
    audio_file_path = None  # Inicializar la variable

    try:
        _, file_extension = os.path.splitext(file_path)

        if file_extension.lower() in ['.mp4', '.avi', '.mov', '.mkv']:
            audio_file_path = extract_audio_from_video(file_path)
        else:
            audio_file_path = file_path

        url = "https://api.audd.io/"
        
        with open(audio_file_path, 'rb') as audio_file:
            data = {
                'api_token': api_token,
                'return': 'timecode,deezer',
            }
            files = {
                'file': audio_file
            }
            response = requests.post(url, data=data, files=files)
        
        if response.status_code == 200:
            result = response.json()
            if result['status'] == 'success' and result['result']:
                song = result['result']['title']
                artist = result['result']['artist']
                return f"{song},{artist}"
            else:
                return "No se pudo identificar la canción"
        else:
            return f"Error: {response.status_code}"

    finally:
        if audio_file_path and os.path.exists(audio_file_path):
            os.remove(audio_file_path)

# reconocimiento_music/views.py
def redirect_to_recognition(request):
    return redirect('/reconocimiento/')

def upload(request):
    if request.method == 'POST' and request.FILES['audio_file']:
        audio_file = request.FILES['audio_file']
        fs = FileSystemStorage()
        file_path = fs.save(audio_file.name, audio_file)
        file_path = os.path.join(settings.MEDIA_ROOT, file_path)
        
        api_token = "b6c56fd5fd469788f481bab9aee0d033"  # Reemplaza esto con tu clave de API
        song_info = identify_song(file_path, api_token)
        print("ESTA ES LOS DATOS: " + song_info)  # Esto te mostrará qué valores estás recibiendo.

        # Dividir la información en título y artista para usar en la plantilla
        if song_info:
            song_info = song_info.strip()  # Limpiar espacios al inicio y final

            # Intentar hacer el split de manera segura
            match = re.match(r'(.+?),\s*(.+)', song_info)  # Usar regex para capturar título y artista
            if match:
                title, artist = match.groups()
            else:
                title, artist = "Desconocido", "Desconocido"  # Valores por defecto en caso de error
            
            return render(request, 'reconocimiento_music/upload.html', {
                'song_info': {'title': title, 'artist': artist}
            })
    
    return render(request, 'reconocimiento_music/upload.html')