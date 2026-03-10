from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status

from database import SessionLocal, engine
import models

# This creates movies.db + the movies table automatically on startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# ── Pydantic schema (same as before, no changes needed here) ──────────────────
class MovieRequest(BaseModel):
    id: Optional[int] = Field(description='ID is not needed on create', default=None)
    title:    str = Field(min_length=1, max_length=100)
    director: str = Field(min_length=1, max_length=100)
    genre:    str = Field(min_length=1, max_length=50)
    year:     int = Field(gt=1887, lt=2031)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Inception",
                "director": "Christopher Nolan",
                "genre": "sci-fi",
                "year": 2010
            }
        }
    }


# ── DB session dependency ─────────────────────────────────────────────────────
# FastAPI calls this for every request → gives a db session → closes it after
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ── Seed starter data on first run ────────────────────────────────────────────
def seed_movies(db: Session):
    if db.query(models.Movie).count() == 0:
        starter = [
            models.Movie(title='Inception',       director='Christopher Nolan',   genre='sci-fi',     year=2010),
            models.Movie(title='The Dark Knight', director='Christopher Nolan',   genre='action',     year=2008),
            models.Movie(title='Interstellar',    director='Christopher Nolan',   genre='sci-fi',     year=2014),
            models.Movie(title='Titanic',         director='James Cameron',        genre='romance',    year=1997),
            models.Movie(title='Forrest Gump',    director='Robert Zemeckis',      genre='drama',      year=1994),
            models.Movie(title='Gladiator',       director='Ridley Scott',          genre='historical', year=2000),
            models.Movie(title='The Godfather',   director='Francis Ford Coppola', genre='crime',      year=1972),
            models.Movie(title='Parasite',        director='Bong Joon-ho',          genre='thriller',   year=2019),
            models.Movie(title='La La Land',      director='Damien Chazelle',       genre='musical',    year=2016),
        ]
        db.add_all(starter)
        db.commit()

@app.on_event("startup")
def on_startup():
    db = SessionLocal()
    try:
        seed_movies(db)
    finally:
        db.close()


# ── Routes (same URLs, same logic — just db instead of MOVIES list) ───────────

@app.get('/', status_code=status.HTTP_200_OK)
async def root():
    return {"message": "Welcome to the Movie API"}


@app.get('/movies', status_code=status.HTTP_200_OK)
async def read_all_movies(db: Session = Depends(get_db)):
    return db.query(models.Movie).all()


@app.get("/movies/bydirector/", status_code=status.HTTP_200_OK)
async def read_movies_by_director(director: str = Query(min_length=1), db: Session = Depends(get_db)):
    movies = db.query(models.Movie).filter(models.Movie.director.ilike(director)).all()
    if not movies:
        raise HTTPException(status_code=404, detail=f"No movies found for director '{director}'")
    return movies


@app.get("/movies/bygenre/", status_code=status.HTTP_200_OK)
async def read_movies_by_genre(genre: str = Query(min_length=1), db: Session = Depends(get_db)):
    movies = db.query(models.Movie).filter(models.Movie.genre.ilike(genre)).all()
    if not movies:
        raise HTTPException(status_code=404, detail=f"No movies found for genre '{genre}'")
    return movies


@app.get("/movies/byyear/", status_code=status.HTTP_200_OK)
async def read_movies_by_year(year: int = Query(gt=1887, lt=2031), db: Session = Depends(get_db)):
    movies = db.query(models.Movie).filter(models.Movie.year == year).all()
    if not movies:
        raise HTTPException(status_code=404, detail=f"No movies found for year {year}")
    return movies


@app.get("/movies/director_genre/", status_code=status.HTTP_200_OK)
async def read_director_and_genre(
    director: str = Query(min_length=1),
    genre:    str = Query(min_length=1),
    db: Session = Depends(get_db)
):
    movies = db.query(models.Movie).filter(
        models.Movie.director.ilike(director),
        models.Movie.genre.ilike(genre)
    ).all()
    if not movies:
        raise HTTPException(status_code=404, detail=f"No movies found for director '{director}' and genre '{genre}'")
    return movies


@app.get("/movies/search/", status_code=status.HTTP_200_OK)
async def search_movies(q: str = Query(min_length=1), db: Session = Depends(get_db)):
    term = f"%{q}%"
    movies = db.query(models.Movie).filter(
        models.Movie.title.ilike(term)    |
        models.Movie.director.ilike(term) |
        models.Movie.genre.ilike(term)
    ).all()
    if not movies:
        raise HTTPException(status_code=404, detail=f"No movies found for '{q}'")
    return movies


@app.get('/movies/{movie_id}', status_code=status.HTTP_200_OK)
async def read_movie(movie_id: int = Path(gt=0), db: Session = Depends(get_db)):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail='Movie not found')
    return movie


@app.post("/movies/create_movie", status_code=status.HTTP_201_CREATED)
async def create_movie(movie_request: MovieRequest, db: Session = Depends(get_db)):
    existing = db.query(models.Movie).filter(models.Movie.title.ilike(movie_request.title)).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Movie '{movie_request.title}' already exists")
    new_movie = models.Movie(**movie_request.model_dump(exclude={"id"}))
    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)
    return new_movie


@app.put("/movies/update_movie", status_code=status.HTTP_204_NO_CONTENT)
async def replace_movie(movie_request: MovieRequest, db: Session = Depends(get_db)):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_request.id).first()
    if not movie:
        raise HTTPException(status_code=404, detail='Movie not found')
    movie.title    = movie_request.title
    movie.director = movie_request.director
    movie.genre    = movie_request.genre
    movie.year     = movie_request.year
    db.commit()


@app.patch("/movies/update_movie", status_code=status.HTTP_204_NO_CONTENT)
async def update_movie(movie_request: MovieRequest, db: Session = Depends(get_db)):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_request.id).first()
    if not movie:
        raise HTTPException(status_code=404, detail='Movie not found')
    if movie_request.title    is not None: movie.title    = movie_request.title
    if movie_request.director is not None: movie.director = movie_request.director
    if movie_request.genre    is not None: movie.genre    = movie_request.genre
    if movie_request.year     is not None: movie.year     = movie_request.year
    db.commit()


@app.delete("/movies/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_movie(movie_id: int = Path(gt=0), db: Session = Depends(get_db)):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail='Movie not found')
    db.delete(movie)
    db.commit()