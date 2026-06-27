# Pastebin API

A Django REST Framework API for storing and sharing syntax-highlighted code snippets.

## Features

- Create, list, retrieve, update, and delete code snippets
- Syntax highlighting via Pygments (`/snippets/{id}/highlight/`)
- Read-only user endpoints (`/users/`, `/users/{id}/`)
- JWT-based authentication with `dj-rest-auth`
- OpenAPI schema and interactive API docs (Swagger UI + ReDoc)

## Tech Stack

- Python 3.12+
- Django 6
- Django REST Framework
- dj-rest-auth + django-allauth
- drf-spectacular
- SQLite (default)

## Getting Started

### 1) Clone and install dependencies

```bash
git clone https://github.com/rhythmd18/pastebin-API.git
cd pastebin-API
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2) Run migrations and start the server

```bash
python manage.py migrate
python manage.py createsuperuser  # optional
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`.

## Authentication

This project is configured to use JWT auth.

- Login: `POST /api/auth/login/`
- Refresh token: `POST /api/auth/token/refresh/`
- Verify token: `POST /api/auth/token/verify/`
- Logout: `POST /api/auth/logout/`
- Current user: `GET /api/auth/user/`
- Registration: `POST /api/auth/registration/`

Use the access token in the `Authorization` header:

```http
Authorization: Bearer <access_token>
```

## Core API Endpoints

- `GET /snippets/` — list snippets
- `POST /snippets/` — create snippet (authenticated)
- `GET /snippets/{id}/` — retrieve snippet
- `PUT/PATCH /snippets/{id}/` — update snippet (owner only)
- `DELETE /snippets/{id}/` — delete snippet (owner only)
- `GET /snippets/{id}/highlight/` — HTML highlighted snippet
- `GET /users/` — list users
- `GET /users/{id}/` — retrieve user

## API Documentation

- OpenAPI schema: `GET /schema/`
- Swagger UI: `GET /schema/swagger-ui/`
- ReDoc: `GET /schema/redoc/`

## Run Tests

```bash
python manage.py test
```
