# Polla Mundialista

Aplicacion de "Polla Mundialista" para un grupo privado de usuarios: registro de predicciones sobre 12 partidos de 2 grupos, calculo automatico de puntos y ranking global.

## Stack

- **Backend:** Python + FastAPI + SQLAlchemy + JWT
- **Base de datos:** SQLite en desarrollo local, PostgreSQL en produccion
- **Frontend:** React + Vite + TailwindCSS
- **Deploy:** Backend + DB en Render, Frontend en Vercel

## Estructura

```
polla-mundialista/
├── backend/
│   ├── app/
│   │   ├── core/        # config y seguridad (JWT, hashing)
│   │   ├── routers/     # auth, matches, admin, leaderboard
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── main.py
│   ├── seed.py          # crea admin + precarga los 12 partidos
│   └── requirements.txt
└── frontend/
    └── src/
        ├── api/
        ├── context/      # AuthContext (JWT)
        ├── components/
        └── pages/
```

## Como levantar el proyecto localmente

### 1. Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env            # ajusta valores si quieres

python seed.py                  # crea el admin y los 12 partidos
uvicorn app.main:app --reload   # http://localhost:8000
```

La documentacion interactiva de la API queda en `http://localhost:8000/docs`.

### 2. Frontend

```bash
cd frontend
npm install
cp .env.example .env            # VITE_API_URL apuntando al backend

npm run dev                     # http://localhost:5173
```

## Credenciales de prueba (generadas por el seeder)

- **Admin:** ver `ADMIN_EMAIL` / `ADMIN_PASSWORD` en `backend/.env`
- **Usuario:** se crea registrandote desde `/register` en el frontend

## Reglas de puntuacion

- 3 puntos: acierto exacto del marcador
- 1 punto: acierto de ganador/empate (sin marcador exacto)
- 0 puntos: fallo

## Deploy

- **URL de la app:** https://polla-mundialista-orcin.vercel.app
- **API / documentación interactiva:** https://polla-mundialista-jtcp.onrender.com/docs
- **Usuario Admin:** admin@admin.com / 123456
- **Usuario de prueba:** no hay uno fijo — cualquier persona puede crear su propia cuenta desde `/register` en el frontend

> Nota: el backend está en el plan free de Render, que "duerme" tras ~15 min de inactividad. La primera petición después de estar dormido puede tardar 30-50 segundos en responder.

