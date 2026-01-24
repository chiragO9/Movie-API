from fastapi import Body, FastAPI, HTTPException

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
    return {"message": "Welcome to the Movie API"} 

@app.get('/movies')  
async def read_all_movies():
    return MOVIES

@app.get("/movies/bydirector/")
async def read_movies_by_director(director: str):
    movies_to_return = []
    for movie in MOVIES:
        if movie.get('director', '').casefold() == director.casefold():
            movies_to_return.append(movie)
    
    if not movies_to_return:
        raise HTTPException(status_code=404, detail=f"No movies found for director '{director}'")
    
    return movies_to_return

@app.get("/movies/bygenre/")
async def read_movies_by_genre(genre: str):
    movies_to_return = []
    for movie in MOVIES:
        if movie.get('genre', '').casefold() == genre.casefold():
            movies_to_return.append(movie)
    
    if not movies_to_return:
        raise HTTPException(status_code=404, detail=f"No movies found for genre '{genre}'")
    
    return movies_to_return

@app.get("/movies/byyear/")
async def read_movies_by_year(year: int):
    movies_to_return = []
    for movie in MOVIES:
        if movie.get('year') == year:
            movies_to_return.append(movie)
    
    if not movies_to_return:
        raise HTTPException(status_code=404, detail=f"No movies found for year {year}")
    
    return movies_to_return

@app.get("/movies/director_genre/")
async def read_director_and_genre(director: str, genre: str):
    movies_to_return = []
    for movie in MOVIES:
        if (movie.get('director', '').casefold() == director.casefold() and 
            movie.get('genre', '').casefold() == genre.casefold()):
            movies_to_return.append(movie)
    
    if not movies_to_return:
        raise HTTPException(status_code=404, detail=f"No movies found for director '{director}' and genre '{genre}'")
    
    return movies_to_return

@app.get("/movies/search/")
async def search_movies(q: str):
    movies_to_return = []
    search_term = q.strip().casefold()
    
    if not search_term:
        raise HTTPException(status_code=400, detail="Search query cannot be empty")
    
    for movie in MOVIES:
        title = movie.get('title', '').casefold()
        director = movie.get('director', '').casefold()
        genre = movie.get('genre', '').casefold()
        
        if search_term in title or search_term in director or search_term in genre:
            movies_to_return.append(movie)
    
    if not movies_to_return:
        raise HTTPException(status_code=404, detail=f"No movies found for search '{q}'")
    
    return movies_to_return

@app.post("/movies/create_movie")
async def create_movie(new_movie=Body()):
    # Basic validation
    required_fields = ['title', 'director', 'genre', 'year']
    for field in required_fields:
        if field not in new_movie:
            raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
    
    # Check if movie already exists
    for movie in MOVIES:
        if movie.get('title', '').casefold() == new_movie.get('title', '').casefold():
            raise HTTPException(status_code=400, detail=f"Movie '{new_movie.get('title')}' already exists")
    
    MOVIES.append(new_movie)
    return {"message": f"Movie '{new_movie.get('title')}' created successfully", "movie": new_movie}



@app.get('/movies/{movie_title}')  
async def read_movie(movie_title: str):
    for movie in MOVIES:
        if movie.get('title', '').casefold() == movie_title.casefold():
            return movie
    raise HTTPException(status_code=404, detail=f"Movie '{movie_title}' not found") 