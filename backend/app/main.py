from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import auth, matches, admin, leaderboard

# Crea las tablas si no existen (para el alcance de esta prueba esto basta;
# en un proyecto real usariamos migraciones de Alembic para todo)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Polla Mundialista API")

# En produccion, reemplaza "*" por la URL exacta del frontend en Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(matches.router)
app.include_router(admin.router)
app.include_router(leaderboard.router)


@app.get("/health")
def health():
    return {"status": "ok"}
