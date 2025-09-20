from fastapi import APIRouter, Depends, HTTPException
from utils.token_manager import create_verification_token, decode_verification_token
from utils.mail_sender import send_verification_email  # lo adaptamos a SendGrid
from models import User  # supongamos que tienes un ORM
from database import db

router = APIRouter()

@router.post("/users/register")
async def register_user(user: dict):
    # 1. Guardar en DB con estado "no verificado"
    new_user = User(email=user["email"], username=user["username"], verified=False)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # 2. Crear token de verificación
    token = create_verification_token(new_user.email)["access_token"]

    # 3. Enviar correo
    await send_verification_email(new_user.email, token)

    return {"msg": "Usuario registrado. Revisa tu correo para verificar la cuenta."}


@router.get("/users/verify-email")
async def verify_email(token: str):
    try:
        email = decode_verification_token(token)
    except HTTPException as e:
        raise e

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    user.verified = True
    db.commit()
    return {"msg": "Correo verificado exitosamente"}
