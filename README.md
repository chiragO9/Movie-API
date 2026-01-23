# 🎬 Movie API

A RESTful API built with FastAPI for managing a movie collection. Features complete CRUD operations, advanced filtering, search functionality, and proper error handling.

## Technologies

- Python 3.8+
- FastAPI
- Uvicorn

## 📦 Installation

1. Clone the repository
```bash
git clone https://github.com/ChiragO9/Movie-API-.git
cd Movie-API-
```

2. Create and activate virtual environment
```bash
# Create virtual environment
python -m venv fastapienv

# Activate on Windows
fastapienv\Scripts\activate

# Activate on Mac/Linux
source fastapienv/bin/activate
```

3. Install dependencies
```bash
pip install fastapi uvicorn
```

## Running the API
```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

**Interactive Documentation:** `http://127.0.0.1:8000/docs`

## Screenshots

### Interactive API Documentation
![API Documentation](images/first.png)
![API Documentation](images/second.png)

# Movie API

A simple FastAPI application for querying a movie database.

## Installation
```bash
pip install fastapi uvicorn
```

## Running the API
```bash
uvicorn main:app --reload
```

API runs at `http://127.0.0.1:8000`

## Endpoints

### `GET /`
Welcome message

### `GET /movies`
Returns all movies

### `GET /movies/{movie_title}`
Get movie by title (case-insensitive)

**Example:** `/movies/inception`

### `GET /movies/bydirector/?director={name}`
Filter movies by director (case-insensitive)

**Example:** `/movies/bydirector/?director=Christopher Nolan`

### `GET /movies/bygenre/?genre={genre}`
Filter movies by genre (case-insensitive)

**Example:** `/movies/bygenre/?genre=sci-fi`

### `GET /movies/byyear/?year={year}`
Filter movies by release year

**Example:** `/movies/byyear/?year=2010`

## Response Format

All endpoints return JSON. Movie objects contain:
- `title` (string)
- `director` (string)
- `genre` (string)
- `year` (integer)

## Error Responses

Returns 404 with detail message when no movies match the query.

## 👤 Author

**Chirag**
- GitHub: [@ChiragO9](https://github.com/ChiragO9)

---

