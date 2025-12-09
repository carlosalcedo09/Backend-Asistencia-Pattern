import base64
import uuid
from django.core.files.base import ContentFile

def decode_base64_file(data):
    """Convierte base64 en archivo listo para FileField"""
    format, imgstr = data.split(';base64,')  # Ej: 'data:image/png;base64,....'
    ext = format.split('/')[-1]  # png, jpg, etc.
    name = f"{uuid.uuid4()}.{ext}"  # nombre aleatorio
    return ContentFile(base64.b64decode(imgstr), name)
