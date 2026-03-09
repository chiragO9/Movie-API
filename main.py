from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()
class Movie:
    id: int
    title: str
    director: str
    genre: str
    year: int

    def __init__(self, id, title, director, genre, year):
        self.id = id
        self.title = title
        self.director = director
        self.genre = genre
        self.year = year
class MovieRequest(BaseModel):
    id: Optional[int] = Field(description='ID is not needed on create', default=None)
    title: str = Field(min_length=1, max_length=100)
    director: str = Field(min_length=1, max_length=100)
    genre: str = Field(min_length=1, max_length=50)
    year: int = Field(gt=1887, lt=2031)

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

MOVIES = [
    Movie(1, 'Inception',       'Christopher Nolan',    'sci-fi',     2010),
    Movie(2, 'The Dark Knight', 'Christopher Nolan',    'action',     2008),
    Movie(3, 'Interstellar',    'Christopher Nolan',    'sci-fi',     2014),
    Movie(4, 'Titanic',         'James Cameron',         'romance',    1997),
    Movie(5, 'Forrest Gump',    'Robert Zemeckis',       'drama',      1994),
    Movie(6, 'Gladiator',       'Ridley Scott',           'historical', 2000),
    Movie(7, 'The Godfather',   'Francis Ford Coppola',  'crime',      1972),
    Movie(8, 'Parasite',        'Bong Joon-ho',           'thriller',   2019),
    Movie(9, 'La La Land',      'Damien Chazelle',        'musical',    2016),
]


def find_movie_id(movie: Movie):
    movie.id = 1 if len(MOVIES) == 0 else MOVIES[-1].id + 1
    return movie

@app.get('/', status_code=status.HTTP_200_OK)
async def root():
    return {"message": "Welcome to the Movie API"}

@app.get('/movies', status_code=status.HTTP_200_OK)
async def read_all_movies():
    return MOVIES

@app.get("/movies/bydirector/", status_code=status.HTTP_200_OK)
async def read_movies_by_director(director: str = Query(min_length=1)):
    movies_to_return = []
    for movie in MOVIES:
        if movie.director.casefold() == director.casefold():
            movies_to_return.append(movie)
    if not movies_to_return:
        raise HTTPException(status_code=404, detail=f"No movies found for director '{director}'")
    return movies_to_return

@app.get("/movies/bygenre/", status_code=status.HTTP_200_OK)
async def read_movies_by_genre(genre: str = Query(min_length=1)):
    movies_to_return = []
    for movie in MOVIES:
        if movie.genre.casefold() == genre.casefold():
            movies_to_return.append(movie)
    if not movies_to_return:
        raise HTTPException(status_code=404, detail=f"No movies found for genre '{genre}'")
    return movies_to_return

@app.get("/movies/byyear/", status_code=status.HTTP_200_OK)
async def read_movies_by_year(year: int = Query(gt=1887, lt=2031)):
    movies_to_return = []
    for movie in MOVIES:
        if movie.year == year:
            movies_to_return.append(movie)
    if not movies_to_return:
        raise HTTPException(status_code=404, detail=f"No movies found for year {year}")
    return movies_to_return

@app.get("/movies/director_genre/", status_code=status.HTTP_200_OK)
async def read_director_and_genre(
    director: str = Query(min_length=1),
    genre: str = Query(min_length=1)
):
    movies_to_return = []
    for movie in MOVIES:
        if (movie.director.casefold() == director.casefold() and
                movie.genre.casefold() == genre.casefold()):
            movies_to_return.append(movie)
    if not movies_to_return:
        raise HTTPException(status_code=404, detail=f"No movies found for director '{director}' and genre '{genre}'")
    return movies_to_return

@app.get("/movies/search/", status_code=status.HTTP_200_OK)
async def search_movies(q: str = Query(min_length=1)):
    movies_to_return = []
    search_term = q.strip().casefold()
    for movie in MOVIES:
        if (search_term in movie.title.casefold() or
                search_term in movie.director.casefold() or
                search_term in movie.genre.casefold()):
            movies_to_return.append(movie)
    if not movies_to_return:
        raise HTTPException(status_code=404, detail=f"No movies found for '{q}'")
    return movies_to_return

@app.get('/movies/{movie_id}', status_code=status.HTTP_200_OK)
async def read_movie(movie_id: int = Path(gt=0)):
    for movie in MOVIES:
        if movie.id == movie_id:
            return movie
    raise HTTPException(status_code=404, detail='Movie not found')

@app.post("/movies/create_movie", status_code=status.HTTP_201_CREATED)
async def create_movie(movie_request: MovieRequest):
    for movie in MOVIES:
        if movie.title.casefold() == movie_request.title.casefold():
            raise HTTPException(status_code=400, detail=f"Movie '{movie_request.title}' already exists")
    new_movie = Movie(**movie_request.model_dump())
    MOVIES.append(find_movie_id(new_movie))

@app.put("/movies/update_movie", status_code=status.HTTP_204_NO_CONTENT)
async def replace_movie(movie_request: MovieRequest):
    movie_changed = False
    for i in range(len(MOVIES)):
        if MOVIES[i].id == movie_request.id:
            MOVIES[i] = Movie(**movie_request.model_dump())
            movie_changed = True
    if not movie_changed:
        raise HTTPException(status_code=404, detail='Movie not found')

@app.patch("/movies/update_movie", status_code=status.HTTP_204_NO_CONTENT)
async def update_movie(movie_request: MovieRequest):
    movie_changed = False
    for i in range(len(MOVIES)):
        if MOVIES[i].id == movie_request.id:
            movie = MOVIES[i]
            # Only update fields that were actually sent (not None)
            if movie_request.title is not None:
                movie.title = movie_request.title
            if movie_request.director is not None:
                movie.director = movie_request.director
            if movie_request.genre is not None:
                movie.genre = movie_request.genre
            if movie_request.year is not None:
                movie.year = movie_request.year
            movie_changed = True
    if not movie_changed:
        raise HTTPException(status_code=404, detail='Movie not found')

@app.delete("/movies/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_movie(movie_id: int = Path(gt=0)):
    movie_changed = False
    for i in range(len(MOVIES)):
        if MOVIES[i].id == movie_id:
            MOVIES.pop(i)
            movie_changed = True
            break
    if not movie_changed:
        raise HTTPException(status_code=404, detail='Movie not found')