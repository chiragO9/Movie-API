# 🎬 Movie API

A RESTful API built with FastAPI for managing a movie collection. Features complete CRUD operations, advanced filtering, search functionality, and proper error handling.

## Technologies

- Python 3.8+
- FastAPI
- Uvicorn
- Pydantic

## Project Structure
```
MOVIE-API/
├── main.py          ← API routes, models, and logic
└── requirements.txt
```

## 📦 Installation

1. **Clone the repository**
```bash
git clone https://github.com/ChiragO9/Movie-API-.git
cd Movie-API-
```

2. **Create and activate virtual environment**
```bash
# Create virtual environment
python -m venv fastapienv

# Activate on Windows
fastapienv\Scripts\activate

# Activate on Mac/Linux
source fastapienv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

Or manually:
```bash
pip install fastapi uvicorn
```

## Running the API
```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

**Interactive Documentation:** `http://127.0.0.1:8000/docs`

> **Note:** Data is stored in-memory and will reset on server restart.

## API Endpoints

### Root
- **`GET /`**
  - Returns welcome message
  - **Response:** `{"message": "Welcome to the Movie API"}`

### Get All Movies
- **`GET /movies`**
  - Returns all movies
  - **Response:** Array of movie objects

### Get Movie by ID
- **`GET /movies/{movie_id}`**
  - Get a specific movie by its ID
  - **Example:** `/movies/1`
  - **Path Param:** `movie_id` must be a positive integer
  - **Response:** Single movie object or 404 error

### Filter by Director
- **`GET /movies/bydirector/?director={name}`**
  - Filter movies by director name (case-insensitive)
  - **Example:** `/movies/bydirector/?director=Christopher Nolan`
  - **Response:** Array of matching movies or 404 error

### Filter by Genre
- **`GET /movies/bygenre/?genre={genre}`**
  - Filter movies by genre (case-insensitive)
  - **Example:** `/movies/bygenre/?genre=sci-fi`
  - **Response:** Array of matching movies or 404 error

### Filter by Year
- **`GET /movies/byyear/?year={year}`**
  - Filter movies by release year (valid range: 1888–2030)
  - **Example:** `/movies/byyear/?year=2010`
  - **Response:** Array of matching movies or 404 error

### Filter by Director AND Genre
- **`GET /movies/director_genre/?director={name}&genre={genre}`**
  - Filter movies by both director and genre (case-insensitive)
  - **Example:** `/movies/director_genre/?director=Christopher Nolan&genre=sci-fi`
  - **Response:** Array of matching movies or 404 error

### Search Movies
- **`GET /movies/search/?q={query}`**
  - Search across title, director, and genre (case-insensitive)
  - **Example:** `/movies/search/?q=nolan`
  - **Response:** Array of matching movies or 404 error

### Create Movie
- **`POST /movies/create_movie`**
  - Add a new movie (ID is auto-assigned)
  - **Request Body:**
```json
{
  "title": "Movie Title",
  "director": "Director Name",
  "genre": "Genre",
  "year": 2024
}
```
  - **Response:** `201 Created`
  - **Validation:**
    - `title` and `director`: 1–100 characters
    - `genre`: 1–50 characters
    - `year`: between 1888 and 2030
    - Movie title must be unique (400 error if duplicate)

### Replace Movie (Full Update)
- **`PUT /movies/update_movie`**
  - Fully replace an existing movie by ID
  - **Request Body:** Same as Create, but `id` is required
```json
{
  "id": 1,
  "title": "Updated Title",
  "director": "Updated Director",
  "genre": "Updated Genre",
  "year": 2024
}
```
  - **Response:** `204 No Content` or 404 error

### Update Movie (Partial Update)
- **`PATCH /movies/update_movie`**
  - Partially update an existing movie — only provided fields are changed
  - **Request Body:** `id` is required, all other fields are optional
```json
{
  "id": 1,
  "genre": "thriller"
}
```
  - **Response:** `204 No Content` or 404 error

### Delete Movie
- **`DELETE /movies/{movie_id}`**
  - Delete a movie by its ID
  - **Example:** `/movies/3`
  - **Path Param:** `movie_id` must be a positive integer
  - **Response:** `204 No Content` or 404 error

## Response Format

All endpoints return JSON. Movie objects contain:
- `id` (integer) — Auto-assigned unique identifier
- `title` (string) — Movie title
- `director` (string) — Director name
- `genre` (string) — Movie genre
- `year` (integer) — Release year

**Example Movie Object:**
```json
{
  "id": 1,
  "title": "Inception",
  "director": "Christopher Nolan",
  "genre": "sci-fi",
  "year": 2010
}
```

## Error Responses

- **404 Not Found** — No movies match the query or movie doesn't exist
- **400 Bad Request** — Missing required fields, duplicate movie title, or invalid input
- **422 Unprocessable Entity** — Request body fails validation constraints

**Error Response Format:**
```json
{
  "detail": "Error message describing the issue"
}
```

## Sample Movie Data

The API comes pre-loaded with 9 movies:

| # | Title | Director | Genre | Year |
|---|-------|----------|-------|------|
| 1 | Inception | Christopher Nolan | sci-fi | 2010 |
| 2 | The Dark Knight | Christopher Nolan | action | 2008 |
| 3 | Interstellar | Christopher Nolan | sci-fi | 2014 |
| 4 | Titanic | James Cameron | romance | 1997 |
| 5 | Forrest Gump | Robert Zemeckis | drama | 1994 |
| 6 | Gladiator | Ridley Scott | historical | 2000 |
| 7 | The Godfather | Francis Ford Coppola | crime | 1972 |
| 8 | Parasite | Bong Joon-ho | thriller | 2019 |
| 9 | La La Land | Damien Chazelle | musical | 2016 |

## Author

**Chirag**
- GitHub: [@ChiragO9](https://github.com/ChiragO9)
