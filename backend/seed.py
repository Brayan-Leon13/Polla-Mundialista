"""
Seeder: crea el usuario Admin y precarga 12 partidos de 2 grupos.
Ejecutar con: python seed.py
"""
from datetime import datetime, timedelta

from app.core.config import settings
from app.core.security import hash_password
from app.database import Base, engine, SessionLocal
from app.models import User, Role, Group, Match

Base.metadata.create_all(bind=engine)

db = SessionLocal()

# --- Admin ---
admin = db.query(User).filter(User.email == settings.admin_email).first()
if not admin:
    admin = User(
        email=settings.admin_email,
        password_hash=hash_password(settings.admin_password),
        role=Role.admin,
    )
    db.add(admin)
    print(f"Admin creado: {settings.admin_email} / {settings.admin_password}")
else:
    admin.password_hash = hash_password(settings.admin_password)
    admin.role = Role.admin
    print(f"Admin ya existia, password reseteado: {settings.admin_email} / {settings.admin_password}")

# --- Grupos ---
group_a = db.query(Group).filter(Group.name == "Grupo A").first()
if not group_a:
    group_a = Group(name="Grupo A")
    db.add(group_a)

group_b = db.query(Group).filter(Group.name == "Grupo B").first()
if not group_b:
    group_b = Group(name="Grupo B")
    db.add(group_b)

db.commit()
db.refresh(group_a)
db.refresh(group_b)

# --- 12 partidos (6 por grupo) ---
if db.query(Match).count() == 0:
    base_date = datetime.utcnow() + timedelta(days=7)

    group_a_teams = ["Argentina", "Mexico", "Polonia", "Arabia Saudita"]
    group_b_teams = ["Francia", "Australia", "Dinamarca", "Tunez"]

    def round_robin_pairs(teams):
        pairs = []
        for i in range(len(teams)):
            for j in range(i + 1, len(teams)):
                pairs.append((teams[i], teams[j]))
        return pairs

    matches_data = []
    for group, teams in [(group_a, group_a_teams), (group_b, group_b_teams)]:
        for home, away in round_robin_pairs(teams):
            matches_data.append((group, home, away))

    for idx, (group, home, away) in enumerate(matches_data):
        match = Match(
            group_id=group.id,
            home_team=home,
            away_team=away,
            match_date=base_date + timedelta(days=idx),
        )
        db.add(match)

    db.commit()
    print(f"{len(matches_data)} partidos creados (6 en Grupo A, 6 en Grupo B).")
else:
    print("Ya existian partidos, no se recrearon.")

db.close()
print("Seed completado.")
