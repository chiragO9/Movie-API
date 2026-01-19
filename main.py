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

@app.get('/')
async def root():
  return "Welcome to the Movie API"

@app.get('/movies')
async def read_all_movies():
  return MOVIES

@app.get('/movies/{movie_title}')
async def read_movie(movie_title : str):
  for movie in MOVIES:
    if movie.get('title', '').casefold() == movie_title.casefold():
      return movie
  return {"Error" :f"{movie_title}  Movie not found"}

@app.get('/movies/byDirector/')
async def read_movie_by_director(director : str):
    movies_to_return = []
    
    for movie in MOVIES:
        if movie.get('director', '').casefold() == director.casefold():
            movies_to_return.append(movie)
  
    if not movies_to_return:
        return {"Error": f"No movies found for director '{director}'"}
    
    return movies_to_return


@app.get('/movies/byGenre/')  
async def read_movies_by_genre(genre: str):
    movies_to_return = []
    
    for movie in MOVIES:
        if movie.get('genre', '').casefold() == genre.casefold():
            movies_to_return.append(movie)
    
    if not movies_to_return:
        return {"Error": f"No movies found for genre '{genre}'"}
    
    return movies_to_return

@app.get('/movies/byYear/')
async def read_movies_by_year(year: int):
    movies_to_return = []
    for movie in MOVIES:
        if movie.get('year',0) == 'year':
            movies_to_return.append(movie)
    return movies_to_return
