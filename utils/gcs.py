import os, json
from fastapi import HTTPException, UploadFile
from google.cloud import storage
from google.oauth2 import service_account

credentials_json = os.getenv("GOOGLE_CREDENTIALS")

if not credentials_json:
    raise RuntimeError("La variable de entorno GOOGLE_CREDENTIALS no está definida")

# Convertir de JSON a dict
credentials_dict = json.loads(credentials_json)

# Asegurarse de que las nuevas líneas de la clave privada se interpreten bien
credentials_dict["private_key"] = credentials_dict["private_key"].replace("\\n", "\n")

# Crear credenciales y cliente de GCS
credentials = service_account.Credentials.from_service_account_info(credentials_dict)
storage_client = storage.Client(credentials=credentials, project=credentials.project_id)

BUCKET_NAME = os.getenv("BUCKET_NAME")
