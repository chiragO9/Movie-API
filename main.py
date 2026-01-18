from fastapi import Body, FastAPI

app = FastAPI()

MOVIES = [
    {'title': 'Inception', 'director': 'Christopher Nolan', 'genre': 'sci-fi', 'year': 2010},
    {'title': 'The Dark Knight', 'director': 'Christopher Nolan', 'genre': 'action', 'year': 2008},
    {'title': 'Interstellar', 'director': 'Christopher Nolan', 'genre': 'sci-fi', 'year': 2014},

    {'title': 'Titanic', 'director': 'James Cameron', 'genre': 'romance', 'year': 1997},
    {'title': 'Forrest Gump', 'director': 'Robert Zemeckis', 'genre': 'drama', 'year': 1994},
    {'title': 'Gladiator', 'director': 'Ridley Scott', 'genre': 'historical', 'year': 2000},
    {'title': 'The Godfather', 'director': 'Francis Ford Coppola', 'genre': 'crime', 'year': 1972},
    {'title': 'Parasite', 'director': 'Bong Joon-ho', 'genre': 'thriller', 'year': 2019},
    {'title': 'La La Land', 'director': 'Damien Chazelle', 'genre': 'musical', 'year': 2016},
]

@app.get('/movies')
async def read_all_movies():
  return MOVIES