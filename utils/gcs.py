import os
import json
from fastapi import HTTPException, UploadFile
from google.cloud import storage
from google.oauth2 import service_account

# Leer credenciales desde variable de entorno
credentials_json = os.getenv("GOOGLE_CREDENTIALS")

if not credentials_json:
    raise RuntimeError("La variable de entorno GOOGLE_CREDENTIALS no está definida")

# Convertir de JSON a dict
credentials_dict = json.loads(credentials_json)

# Corregir la clave privada (\n -> saltos de línea reales)
credentials_dict["private_key"] = credentials_dict["private_key"].replace("\\n", "\n")
print(credentials_dict["private_key"][:100])  # para ver inicio
print(credentials_dict["private_key"][-50:])  # para ver fin
# Crear credenciales y cliente de GCS
credentials = service_account.Credentials.from_service_account_info(credentials_dict)
storage_client = storage.Client(credentials=credentials, project=credentials.project_id)

# Nombre del bucket
BUCKET_NAME = os.getenv("BUCKET_NAME")
if not BUCKET_NAME:
    raise RuntimeError("La variable de entorno BUCKET_NAME no está definida")

def generate_unique_filename(bucket, filename):
    base_name, ext = os.path.splitext(filename)
    index = 1
    new_filename = filename

    while bucket.blob(new_filename).exists():
        new_filename = f"{base_name}({index}){ext}"
        index += 1

    return new_filename

def upload_file(file: UploadFile):
    bucket = storage_client.bucket(BUCKET_NAME)
    unique_name = generate_unique_filename(bucket, file.filename)
    blob = bucket.blob(unique_name)
    blob.upload_from_file(file.file, content_type=file.content_type)
    return {
        "url": f"https://storage.googleapis.com/{BUCKET_NAME}/{unique_name}",
        "filename": unique_name,
    }


def delete_file(blob_name: str) -> None:
    """
    Elimina un archivo de Google Cloud Storage.
    """
    try:
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(blob_name)
        blob.delete()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar archivo: {e}")
