# Pastebin API

A RESTful API for a pastebin application built with Django and Django REST Framework. Share, store, and display code snippets with automatic syntax highlighting.

## Features

✨ **Core Features**

- 🔐 User authentication and authorization with JWT tokens
- 📝 Create, read, update, and delete code snippets
- 🎨 Automatic syntax highlighting using Pygments
- 👥 User profile management
- 📧 Email verification and password reset functionality
- 🔄 JWT token refresh mechanism
- 📄 Paginated list endpoints
- 🛡️ Secure HTTP-only cookie storage for tokens

## Tech Stack

| Component         | Technology                                 |
| ----------------- | ------------------------------------------ |
| Backend           | Django 6.0.3                               |
| REST API          | Django REST Framework 3.17.1               |
| Authentication    | djangorestframework-simplejwt 5.5.1        |
| User Management   | dj-rest-auth 7.2.0, django-allauth 65.15.0 |
| API Documentation | drf-spectacular 0.29.0                     |
| Code Highlighting | Pygments 2.17.2                            |
| Database          | SQLite (or PostgreSQL for production)      |
| Python            | 3.10+                                      |

## Quick Start

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Installation

1. **Clone the repository**

```bash
git clone <repository-url>
cd pastebin-API
```

2. **Create and activate virtual environment**

```bash
# On Windows
python -m venv .venv
.venv\Scripts\activate

# On macOS/Linux
python -m venv .venv
source .venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Apply database migrations**

```bash
python manage.py migrate
```

5. **Create a superuser (admin account)**

```bash
python manage.py createsuperuser
```

6. **Run the development server**

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000`

## Project Structure

```
pastebin-API/
├── django_project/          # Main Django project settings
│   ├── settings.py          # Django settings and configuration
│   ├── urls.py              # Main URL routing
│   ├── wsgi.py              # Production WSGI config
│   └── asgi.py              # Production ASGI config
├── snippets/                # Snippets app (main API functionality)
│   ├── models.py            # Database models (Snippet model)
│   ├── serializers.py       # DRF serializers
│   ├── views.py             # API views and viewsets
│   ├── urls.py              # App-specific URL routing
│   ├── permissions.py       # Custom permission classes
│   ├── admin.py             # Django admin config
│   ├── tests.py             # Unit tests
│   └── migrations/          # Database migration files
├── docs/                    # Documentation
│   └── API_DOCUMENTATION.md # Complete API documentation
├── manage.py                # Django management script
├── db.sqlite3               # SQLite database
├── schema.yml               # OpenAPI 3.0.3 schema
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

## API Documentation

For complete API documentation with all endpoints, request/response examples, and frontend integration guides, see [docs/API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md).

### Quick API Reference

**Base URL:** `http://localhost:8000`

#### Authentication Endpoints

- `POST /api/auth/registration/` - Register new user
- `POST /api/auth/login/` - Login user
- `POST /api/auth/logout/` - Logout user
- `GET /api/auth/user/` - Get current user details
- `PUT/PATCH /api/auth/user/` - Update user profile
- `POST /api/auth/password/change/` - Change password
- `POST /api/auth/password/reset/` - Request password reset
- `POST /api/auth/password/reset/confirm/` - Confirm password reset

#### Snippets Endpoints

- `GET /snippets/` - List all snippets (paginated)
- `POST /snippets/` - Create new snippet
- `GET /snippets/{id}/` - Get snippet details
- `PUT/PATCH /snippets/{id}/` - Update snippet
- `DELETE /snippets/{id}/` - Delete snippet
- `GET /snippets/{id}/highlight/` - Get highlighted HTML

#### Users Endpoints

- `GET /users/` - List all users
- `GET /users/{id}/` - Get user details

#### Documentation

- `GET /schema/` - OpenAPI 3.0.3 schema
- `GET /` - API root with resource links

## Configuration

### Environment Variables

Create a `.env` file in the project root (optional):

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

### Django Settings

Key settings in `django_project/settings.py`:

| Setting                    | Purpose                                        |
| -------------------------- | ---------------------------------------------- |
| `DEBUG`                    | Enable/disable debug mode                      |
| `ALLOWED_HOSTS`            | Allowed host names                             |
| `INSTALLED_APPS`           | Installed Django apps                          |
| `DATABASES`                | Database configuration                         |
| `REST_FRAMEWORK`           | DRF configuration (pagination, authentication) |
| `REST_AUTH`                | JWT authentication settings                    |
| `DRF_SPECTACULAR_SETTINGS` | API schema settings                            |

## Authentication

### How Authentication Works

1. **Registration**: User creates account via `/api/auth/registration/`
2. **Login**: User logs in via `/api/auth/login/` and receives JWT tokens
3. **Cookie Storage**: Tokens stored in HTTP-only cookies automatically
4. **Requests**: Subsequent requests automatically include cookies
5. **Token Refresh**: Access tokens can be refreshed via `/api/auth/token/refresh/`

### Token Types

- **Access Token**: Short-lived token (used for API requests)
- **Refresh Token**: Long-lived token (used to get new access tokens)

Both are stored in secure HTTP-only cookies by default.

## Usage Examples

### Register a New User

```bash
curl -X POST http://localhost:8000/api/auth/registration/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password1": "secure_password",
    "password2": "secure_password"
  }'
```

### Login

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{
    "username": "john_doe",
    "password": "secure_password"
  }'
```

### Create a Snippet

```bash
curl -X POST http://localhost:8000/snippets/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "title": "Hello World in Python",
    "code": "print(\"Hello, World!\")",
    "language": "python",
    "style": "friendly",
    "linenos": true
  }'
```

### List Snippets

```bash
curl http://localhost:8000/snippets/
```

### Get Specific Snippet

```bash
curl http://localhost:8000/snippets/1/
```

### Get Highlighted Snippet

```bash
curl http://localhost:8000/snippets/1/highlight/
```

### Update Snippet

```bash
curl -X PATCH http://localhost:8000/snippets/1/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "title": "Updated Title"
  }'
```

### Delete Snippet

```bash
curl -X DELETE http://localhost:8000/snippets/1/ \
  -b cookies.txt
```

## Admin Interface

The Django admin interface is available at `http://localhost:8000/admin/`

**Features:**

- Manage users and snippets
- View activity history
- Configure site settings

Login with the superuser account created during setup.

## Development

### Running Tests

```bash
python manage.py test
```

### Running Tests with Coverage

```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

### Database Migrations

Create new migration after model changes:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Linting and Formatting

```bash
# Install linting tools (optional)
pip install flake8 black

# Format code
black .

# Lint code
flake8 .
```

## Building a Frontend

This API is designed to be used with a frontend built in React, Vue, Angular, or any other modern framework.

**Key points for frontend development:**

1. **Authentication**: After login, tokens are automatically stored in cookies. No manual token management needed.

2. **CORS**: If your frontend is on a different domain, configure CORS in Django settings.

3. **Base URL**: Configure your frontend to use `http://localhost:8000` (or your deployed URL).

4. **API Documentation**: Use [docs/API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md) for complete endpoint details.

5. **Error Handling**: Implement error handling for common HTTP status codes (400, 401, 403, 404, 500).

6. **Pagination**: Handle paginated responses using `next` and `previous` URLs.

7. **Highlighted Code**: The API provides pre-rendered HTML in the `highlighted` field. Display this as HTML, not plain text.

## Deployment

### Production Checklist

- [ ] Set `DEBUG = False` in settings
- [ ] Set a strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up proper database (PostgreSQL recommended)
- [ ] Configure email backend for password resets
- [ ] Enable HTTPS
- [ ] Set up static/media file serving
- [ ] Use a production WSGI server (Gunicorn, uWSGI)
- [ ] Set up proper logging

### Deploy with Gunicorn

```bash
pip install gunicorn

# Run with Gunicorn
gunicorn django_project.wsgi:application --bind 0.0.0.0:8000
```

### Deploy with Docker

Include a `Dockerfile` and `docker-compose.yml` for containerized deployment (not included in this repo).

## Troubleshooting

### Common Issues

**Issue:** `ModuleNotFoundError: No module named 'django'`

- **Solution:** Ensure virtual environment is activated and dependencies are installed
  ```bash
  pip install -r requirements.txt
  ```

**Issue:** Database errors on first run

- **Solution:** Run migrations
  ```bash
  python manage.py migrate
  ```

**Issue:** CORS errors when connecting from frontend

- **Solution:** Install and configure django-cors-headers
  ```bash
  pip install django-cors-headers
  ```
  Then add to `INSTALLED_APPS` and `MIDDLEWARE` in settings.py

**Issue:** Authentication not working

- **Solution:** Verify JWT settings in settings.py and ensure cookies are enabled in frontend

**Issue:** Email not sending

- **Solution:** Configure proper EMAIL_BACKEND in settings.py for development or production

## API Security

### Implemented Security Features

✅ **Authentication:** JWT-based authentication with secure HTTP-only cookies  
✅ **Authorization:** Permission checks for resource ownership  
✅ **CSRF Protection:** Django's built-in CSRF middleware  
✅ **Password Security:** Django's password hashers and validators  
✅ **Email Verification:** Optional email verification for registration

### Security Best Practices

1. Always use HTTPS in production
2. Store sensitive data in environment variables
3. Regularly update dependencies
4. Use strong SECRET_KEY
5. Enable rate limiting in production
6. Implement proper logging and monitoring
7. Use environment-specific settings

## Performance

### Optimization Tips

1. **Database**: Use indexes on frequently queried fields
2. **Caching**: Implement caching for highlighted snippets
3. **Pagination**: Use pagination for large datasets (already implemented)
4. **Database Connection**: Use connection pooling in production
5. **CDN**: Serve static files from a CDN

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write/update tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues, questions, or suggestions:

- Create an issue on GitHub
- Check the [docs/API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md) for detailed API information
- Review the troubleshooting section above

## API Schema

The OpenAPI 3.0.3 schema for this API is available at:

- **Endpoint**: `GET /schema/`
- **File**: [schema.yml](schema.yml)

This schema can be used to generate API clients or documentation with tools like:

- Swagger UI
- ReDoc
- OpenAPI Generator
- Postman

## Changelog

### Version 1.0.0

- Initial release
- User authentication with JWT
- Snippet CRUD operations
- Syntax highlighting with Pygments
- User management endpoints
- Email verification
- Password reset functionality

## Roadmap

Future enhancements planned:

- [ ] Social authentication (GitHub, Google)
- [ ] Snippet sharing and collaboration
- [ ] Tags and categories for snippets
- [ ] API rate limiting
- [ ] Advanced search functionality
- [ ] Snippet forking/cloning
- [ ] Comments on snippets
- [ ] User profiles with bio
- [ ] Mobile app support
- [ ] Analytics and usage statistics

## Getting Help

- 📖 Read the [docs/API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md) for complete API reference
- 🐛 Check existing issues and discussions
- 💬 Create a new issue with detailed information

---

**Last Updated:** March 31, 2026  
**API Version:** 1.0.0  
**Django Version:** 6.0.3  
**Python Version:** 3.10+
