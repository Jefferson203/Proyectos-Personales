import yt_dlp
from urllib.parse import urlparse, urlunparse

def limpiar_url(url):
    # Separar los componentes de la URL y eliminar los parámetros adicionales
    url_parsed = urlparse(url)
    url_limpia = urlunparse((url_parsed.scheme, url_parsed.netloc, url_parsed.path, '', '', ''))
    return url_limpia

def descargar_video(url, formato='mp4'):
    # Limpia la URL antes de procesarla
    url = limpiar_url(url)
    ydl_opts = {}
    
    # Configura opciones según el formato
    if formato == 'mp3':
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
    elif formato == 'mp4':
        ydl_opts = {
            'format': 'bestvideo+bestaudio',
        }

    # Descarga el video o el audio
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Solicitar la URL y el formato al usuario
url = input("Introduce la URL del video de YouTube: ")
formato = input("¿En qué formato deseas descargar (mp3 o mp4)?: ").lower()

# Validar el formato
if formato in ['mp3', 'mp4']:
    descargar_video(url, formato=formato)
else:
    print("Formato no válido. Por favor, elige 'mp3' o 'mp4'.")
