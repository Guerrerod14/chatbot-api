import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth_route, category_route, faq_route, resource_route, user_route

app = FastAPI()

origins = [
    "https://chatbot-frontend-seven-chi.vercel.app"  # tu frontend en Vercel
    # "http://localhost:3000"  # opcional para pruebas locales
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # usa el dominio, no "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas
app.include_router(user_route.router)
app.include_router(auth_route.router)
app.include_router(resource_route.router)
app.include_router(category_route.router)
app.include_router(faq_route.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}

# 🚀 Punto de entrada para Railway
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
