import yt_dlp
from urllib.parse import urlparse, urlunparse

def limpiar_url(url):
    # Separar los componentes de la URL y eliminar los parámetros adicionales
    url_parsed = urlparse(url)
    url_limpia = urlunparse((url_parsed.scheme, url_parsed.netloc, url_parsed.path, '', '', ''))
    return url_limpia

def mostrar_formatos(url):
    url = limpiar_url(url)
    with yt_dlp.YoutubeDL() as ydl:
        info = ydl.extract_info(url, download=False)  # Extrae información sin descargar
        formatos = info['formats']
        
        # Muestra la lista de formatos disponibles
        print("Formatos disponibles:")
        for fmt in formatos:
            tipo = "Audio/Video"
            if fmt.get('acodec') == 'none':  # Sin audio (solo video)
                tipo = "Video"
            elif fmt.get('vcodec') == 'none':  # Sin video (solo audio)
                tipo = "Audio"
                
            format_note = fmt.get('format_note', 'N/A')
            resolution = fmt.get('resolution', 'N/A')
            
            print(f"ID: {fmt['format_id']} - {tipo} - {fmt['ext']} - {format_note} - {resolution}")
        
        # Añade la opción para convertir a MP3
        print("ID: mp3 - Solo audio - mp3 - Convertir a MP3")

def descargar_video(url, formato_id):
    url = limpiar_url(url)
    
    if formato_id == 'mp3':
        # Opción para descargar solo el audio y convertirlo a MP3
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
    else:
        # Descarga según el ID de formato especificado, con video y audio combinados si es posible
        ydl_opts = {
            'format': f"{formato_id}+bestaudio/best",  # Combina el mejor audio con el formato de video seleccionado
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',  # Asegura la salida en MP4 si es un formato de video
            }],
        }
    
    # Descarga el video o el audio
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Ejemplo de uso
url = input("Introduce la URL del video de YouTube: ")
mostrar_formatos(url)  # Muestra los formatos disponibles

# Solicita el ID del formato deseado
formato_id = input("Introduce el ID del formato en que deseas descargar (o 'mp3' para solo audio en MP3): ")
descargar_video(url, formato_id)
