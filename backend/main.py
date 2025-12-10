# backend/main.py
import os
import psycopg2
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from .schemas import LoginRequest, LoginResponse

from .db import SessionLocal, Base, engine
from . import models, schemas
from .security import hash_password, verify_password

app = FastAPI()

# ---- CORS ----
origins = [
    "http://localhost:5173",  # frontend în browser
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # poți pune ["*"] la început, ca test
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ---------------

Base.metadata.create_all(bind=engine)
DATABASE_URL = os.getenv("DATABASE_URL")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/db-check")
def db_check():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        cur.fetchone()
        cur.close()
        conn.close()
        return {"db": "ok"}
    except Exception as e:
        return {"db": "error", "details": str(e)}


# ---- API listare pentru front ----

@app.get("/api/countries", response_model=list[schemas.CountryBase])
def get_countries(db: Session = Depends(get_db)):
    return db.query(models.Country).order_by(models.Country.name).all()


@app.get("/api/competitions", response_model=list[schemas.CompetitionBase])
def get_competitions(country_id: int | None = None, db: Session = Depends(get_db)):
    q = db.query(models.Competition)
    if country_id is not None:
        q = q.filter(models.Competition.country_id == country_id)
    return q.order_by(models.Competition.name).all()


@app.get("/api/clubs", response_model=list[schemas.ClubBase])
def get_clubs(competition_id: int | None = None, db: Session = Depends(get_db)):
    q = db.query(models.Club)
    if competition_id is not None:
        q = q.filter(models.Club.competition_id == competition_id)
    return q.order_by(models.Club.name).all()


@app.get("/api/top-clubs")
def get_top_clubs(limit: int = 5, db: Session = Depends(get_db)):
    """
    Cele mai valoroase loturi.
    Returnează cluburile ordonate după suma valorilor de piață ale jucătorilor.
    """
    # join Player + Club, grupare pe club
    rows = (
        db.query(
            models.Club.id.label("club_id"),
            models.Club.name.label("club_name"),
            func.coalesce(func.sum(models.Player.market_value), 0).label("total_value"),
            func.count(models.Player.id).label("player_count"),
        )
        .join(models.Player, models.Player.current_club_id == models.Club.id)
        .group_by(models.Club.id, models.Club.name)
        .order_by(desc("total_value"))
        .limit(limit)
        .all()
    )

    # întoarcem ca dict-uri simple
    result = []
    for r in rows:
        result.append(
            {
                "club_id": r.club_id,
                "club_name": r.club_name,
                "total_value": float(r.total_value or 0),
                "player_count": int(r.player_count or 0),
            }
        )

    return result

@app.get("/api/top-players", response_model=list[schemas.PlayerDetails])
def get_top_players(limit: int = 10, db: Session = Depends(get_db)):
    """
    Returnează cei mai valoroși jucători din baza de date.
    Implicit top 10, dar poți schimba cu ?limit=20 etc.
    """
    q = (
        db.query(models.Player)
        .filter(models.Player.market_value.isnot(None))
        .order_by(desc(models.Player.market_value))
        .limit(limit)
    )

    players = q.all()

    result = []
    for p in players:
        result.append(
            {
                "id": p.id,
                "name": p.name,
                "birth_date": p.birth_date,
                "nationality": p.nationality,
                "position_name": p.position.name if p.position else None,
                "club_name": p.current_club.name if p.current_club else None,
                "market_value": p.market_value,
                "competition_name": (
                    p.current_club.competition.name
                    if p.current_club and p.current_club.competition
                    else None
                ),
            }
        )

    return result


@app.get("/api/players", response_model=list[schemas.PlayerDetails])
def get_players(club_id: int | None = None, db: Session = Depends(get_db)):
    q = db.query(models.Player)
    if club_id is not None:
        q = q.filter(models.Player.current_club_id == club_id)

    players = q.order_by(models.Player.name).all()

    result = []
    for p in players:
        result.append(
            {
                "id": p.id,
                "name": p.name,
                "birth_date": p.birth_date,
                "nationality": p.nationality,
                "position_name": p.position.name if p.position else None,
                "club_name": p.current_club.name if p.current_club else None,
                "market_value": p.market_value,
                "competition_name": (
                    p.current_club.competition.name
                    if p.current_club and p.current_club.competition
                    else None
                ),
            }
        )

    return result


@app.get("/api/players/{player_id}", response_model=schemas.PlayerDetails)
def get_player_by_id(player_id: int, db: Session = Depends(get_db)):
    player = (
        db.query(models.Player)
        .filter(models.Player.id == player_id)
        .first()
    )
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    return {
        "id": player.id,
        "name": player.name,
        "birth_date": player.birth_date,
        "nationality": player.nationality,
        "position_name": player.position.name if player.position else None,
        "club_name": player.current_club.name if player.current_club else None,
        "market_value": player.market_value,
        "competition_name": (
            player.current_club.competition.name
            if player.current_club and player.current_club.competition
            else None
        ),
    }


@app.get("/api/clubs/{club_id}", response_model=schemas.ClubDetails)
def get_club_by_id(club_id: int, db: Session = Depends(get_db)):
    club = (
        db.query(models.Club)
        .filter(models.Club.id == club_id)
        .first()
    )
    if not club:
        raise HTTPException(status_code=404, detail="Club not found")

    return {
        "id": club.id,
        "name": club.name,
        "country_name": club.country.name if club.country else None,
        "competition_name": club.competition.name if club.competition else None,
    }

@app.get("/api/search")
def search(q: str, db: Session = Depends(get_db)):
    """
    Caută mai întâi un club după nume (case-insensitive, substring).
    Dacă găsește, returnează lotul clubului.
    Dacă nu, caută un jucător după nume și returnează detalii.
    Răspunsul este un dict simplu, fără response_model.
    """
    if not q or not q.strip():
        raise HTTPException(status_code=400, detail="Query gol")

    pattern = f"%{q.strip()}%"

    # 1) caută club
    club = (
        db.query(models.Club)
        .filter(models.Club.name.ilike(pattern))
        .first()
    )

    if club:
        players = (
            db.query(models.Player)
            .filter(models.Player.current_club_id == club.id)
            .order_by(models.Player.name)
            .all()
        )

        players_out = []
        for p in players:
            players_out.append(
                {
                    "id": p.id,
                    "name": p.name,
                    "birth_date": p.birth_date.isoformat() if p.birth_date else None,
                    "nationality": p.nationality,
                    "position_name": p.position.name if p.position else None,
                    "club_name": p.current_club.name if p.current_club else None,
                    "market_value": str(p.market_value) if p.market_value is not None else None,
                }
            )

        return {
            "type": "club",
            "club": {"id": club.id, "name": club.name},
            "players": players_out,
        }

    # 2) dacă nu e club, caută jucător
    player = (
        db.query(models.Player)
        .filter(models.Player.name.ilike(pattern))
        .first()
    )

    if player:
        player_out = {
            "id": player.id,
            "name": player.name,
            "birth_date": player.birth_date.isoformat() if player.birth_date else None,
            "nationality": player.nationality,
            "position_name": player.position.name if player.position else None,
            "club_name": player.current_club.name if player.current_club else None,
            "market_value": str(player.market_value) if player.market_value is not None else None,
        }

        return {
            "type": "player",
            "player": player_out,
        }

    raise HTTPException(status_code=404, detail="Niciun club sau jucător găsit")


@app.post("/api/register", response_model=schemas.UserOut)
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    # email unic
    existing = db.query(models.User).filter(models.User.email == user_in.email.lower()).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Există deja un cont cu acest email.",
        )

    # telefon unic
    existing_phone = db.query(models.User).filter(models.User.phone == user_in.phone.replace(" ", "")).first()
    if existing_phone:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Există deja un cont cu acest număr de telefon.",
        )

    user = models.User(
        full_name=user_in.full_name.strip(),
        email=user_in.email.lower(),
        phone=user_in.phone.replace(" ", ""),
        password_hash=hash_password(user_in.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.post("/api/login", response_model=schemas.LoginResponse)
def login(payload: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = (
        db.query(models.User)
        .filter(models.User.email == payload.email.lower())
        .first()
    )
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email sau parolă incorecte.",
        )

    token = f"token-{user.id}"

    return schemas.LoginResponse(
        access_token=token,
        user=schemas.UserOut.model_validate(user),  # <-- conversie explicită
    )
