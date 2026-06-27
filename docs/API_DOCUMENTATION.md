# Pastebin API - Complete API Documentation

## Overview

This is a RESTful API for a pastebin application built with Django REST Framework. It provides endpoints for user authentication, snippet management, and user information access. The API uses JWT (JSON Web Token) authentication stored in secure HTTP-only cookies.

**Base URL:** `http://localhost:8000` (or your deployed domain)

**API Version:** 1.0.0

## Authentication

The API uses JWT authentication with the following mechanisms:

- JWT tokens stored in HTTP-only cookies
- Optional Bearer token authentication via Authorization header
- Token refresh capability

### Authentication Methods

1. **Cookie-based (Recommended)**: Tokens automatically stored in HTTP-only cookies after login
2. **Header-based**: Send JWT token in `Authorization: Bearer <token>` header
3. **No Auth**: Some endpoints are publicly accessible

---

## API Endpoints

### 1. Authentication Endpoints

#### 1.1 User Registration

**Endpoint:** `POST /api/auth/registration/`

**Description:** Register a new user account

**Request Body:**

```json
{
  "username": "string",
  "email": "string",
  "password1": "string",
  "password2": "string"
}
```

**Response:** `201 Created`

```json
{
  "key": "token_string",
  "user": {
    "id": 1,
    "username": "string",
    "email": "string"
  }
}
```

**Authentication:** Not required

---

#### 1.2 User Login

**Endpoint:** `POST /api/auth/login/`

**Description:** Authenticate user and receive JWT token

**Request Body:**

```json
{
  "username": "string",
  "password": "string"
}
```

**Response:** `200 OK`

```json
{
  "access": "jwt_token_string",
  "refresh": "refresh_token_string",
  "user": {
    "id": 1,
    "username": "string",
    "email": "string"
  }
}
```

**Headers:** Sets `access` and `refresh` tokens in HTTP-only cookies

**Authentication:** Not required

---

#### 1.3 User Logout

**Endpoint:** `POST /api/auth/logout/`

**Description:** Logout user and invalidate session

**Request Body:** Empty or null

**Response:** `200 OK`

```json
{
  "detail": "Successfully logged out."
}
```

**Authentication:** Required (Authenticated users only)

---

#### 1.4 Get Current User Details

**Endpoint:** `GET /api/auth/user/`

**Description:** Retrieve authenticated user's information

**Response:** `200 OK`

```json
{
  "id": 1,
  "username": "string",
  "email": "string",
  "first_name": "string",
  "last_name": "string"
}
```

**Authentication:** Required

---

#### 1.5 Update Current User

**Endpoint:** `PUT /api/auth/user/`

**Description:** Update authenticated user's information (full update)

**Request Body:**

```json
{
  "username": "string",
  "email": "string",
  "first_name": "string",
  "last_name": "string"
}
```

**Response:** `200 OK` (returns updated user object)

**Authentication:** Required

---

#### 1.6 Partially Update Current User

**Endpoint:** `PATCH /api/auth/user/`

**Description:** Update authenticated user's information (partial update)

**Request Body:** (any of these fields)

```json
{
  "first_name": "string",
  "last_name": "string"
}
```

**Response:** `200 OK` (returns updated user object)

**Authentication:** Required

---

#### 1.7 Change Password

**Endpoint:** `POST /api/auth/password/change/`

**Description:** Change password for authenticated user

**Request Body:**

```json
{
  "old_password": "string",
  "new_password1": "string",
  "new_password2": "string"
}
```

**Response:** `200 OK`

```json
{
  "detail": "Password changed successfully."
}
```

**Authentication:** Required

---

#### 1.8 Request Password Reset

**Endpoint:** `POST /api/auth/password/reset/`

**Description:** Request password reset (sends email with reset link)

**Request Body:**

```json
{
  "email": "string"
}
```

**Response:** `200 OK`

```json
{
  "detail": "Password reset e-mail has been sent."
}
```

**Authentication:** Not required

---

#### 1.9 Confirm Password Reset

**Endpoint:** `POST /api/auth/password/reset/confirm/`

**Description:** Confirm password reset using token from email

**Request Body:**

```json
{
  "uid": "string",
  "token": "string",
  "new_password1": "string",
  "new_password2": "string"
}
```

**Response:** `200 OK`

```json
{
  "detail": "Password has been reset with the new password."
}
```

**Authentication:** Not required

---

#### 1.10 Verify Email

**Endpoint:** `POST /api/auth/registration/verify-email/`

**Description:** Verify email address using verification key

**Request Body:**

```json
{
  "key": "string"
}
```

**Response:** `200 OK`

```json
{
  "detail": "Email verified successfully."
}
```

**Authentication:** Not required

---

#### 1.11 Resend Email Verification

**Endpoint:** `POST /api/auth/registration/resend-email/`

**Description:** Request new email verification (resends verification email)

**Request Body:**

```json
{
  "email": "string"
}
```

**Response:** `201 Created`

```json
{
  "detail": "Verification e-mail sent."
}
```

**Authentication:** Not required

---

#### 1.12 Refresh Access Token

**Endpoint:** `POST /api/auth/token/refresh/`

**Description:** Get a new access token using refresh token

**Request Body:**

```json
{
  "refresh": "refresh_token_string"
}
```

**Response:** `200 OK`

```json
{
  "access": "new_jwt_token_string"
}
```

**Authentication:** Not required

---

#### 1.13 Verify Token

**Endpoint:** `POST /api/auth/token/verify/`

**Description:** Verify if a token is valid

**Request Body:**

```json
{
  "token": "jwt_token_string"
}
```

**Response:** `200 OK` (empty body indicates valid token)

**Authentication:** Not required

---

### 2. Snippets Endpoints

#### 2.1 List All Snippets

**Endpoint:** `GET /snippets/`

**Description:** Get a paginated list of all code snippets

**Query Parameters:**

- `page` (integer): Page number for pagination (default: 1)

**Response:** `200 OK`

```json
{
  "count": 42,
  "next": "http://localhost:8000/snippets/?page=2",
  "previous": null,
  "results": [
    {
      "url": "http://localhost:8000/snippets/1/",
      "id": 1,
      "title": "Hello World in Python",
      "code": "print('Hello, World!')",
      "linenos": false,
      "language": "python",
      "style": "friendly",
      "owner": "john_doe",
      "created": "2025-03-31T10:30:00Z",
      "highlighted": "<div class=\"highlight\">...</div>"
    }
  ]
}
```

**Authentication:** Not required (but recommended for better filtering)

**Example Request:**

```bash
curl http://localhost:8000/snippets/?page=1
```

---

#### 2.2 Create New Snippet

**Endpoint:** `POST /snippets/`

**Description:** Create a new code snippet

**Request Body:**

```json
{
  "title": "string",
  "code": "string",
  "language": "string (e.g., 'python', 'javascript', 'java')",
  "style": "string (e.g., 'friendly', 'monokai', 'vim')",
  "linenos": boolean
}
```

**Response:** `201 Created`

```json
{
  "url": "http://localhost:8000/snippets/1/",
  "id": 1,
  "title": "string",
  "code": "string",
  "linenos": boolean,
  "language": "string",
  "style": "string",
  "owner": "username",
  "created": "2025-03-31T10:30:00Z",
  "highlighted": "string (HTML)"
}
```

**Authentication:** Required

**Example Request:**

```bash
curl -X POST http://localhost:8000/snippets/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "title": "My Python Code",
    "code": "print(\"Hello\")",
    "language": "python",
    "style": "friendly",
    "linenos": true
  }'
```

---

#### 2.3 Retrieve Snippet Details

**Endpoint:** `GET /snippets/{id}/`

**Description:** Get details of a specific snippet

**Path Parameters:**

- `id` (integer): The snippet ID

**Response:** `200 OK`

```json
{
  "url": "http://localhost:8000/snippets/1/",
  "id": 1,
  "title": "string",
  "code": "string",
  "linenos": boolean,
  "language": "string",
  "style": "string",
  "owner": "username",
  "created": "2025-03-31T10:30:00Z",
  "highlighted": "string (HTML)"
}
```

**Authentication:** Not required

**Example Request:**

```bash
curl http://localhost:8000/snippets/1/
```

---

#### 2.4 Get Highlighted Code

**Endpoint:** `GET /snippets/{id}/highlight/`

**Description:** Get the HTML-highlighted version of a snippet's code

**Path Parameters:**

- `id` (integer): The snippet ID

**Response:** `200 OK`

```
<div class="highlight"><span class="k">print</span><span class="p">(</span><span class="s1">'Hello'</span><span class="p">)</span></div>
```

**Authentication:** Not required

**Content-Type:** `text/html`

**Example Request:**

```bash
curl http://localhost:8000/snippets/1/highlight/
```

---

#### 2.5 Update Snippet (Full Update)

**Endpoint:** `PUT /snippets/{id}/`

**Description:** Update entire snippet (all fields required)

**Path Parameters:**

- `id` (integer): The snippet ID

**Request Body:**

```json
{
  "title": "string",
  "code": "string",
  "language": "string",
  "style": "string",
  "linenos": boolean
}
```

**Response:** `200 OK` (returns updated snippet object)

**Authentication:** Required (must be snippet owner)

---

#### 2.6 Update Snippet (Partial Update)

**Endpoint:** `PATCH /snippets/{id}/`

**Description:** Partially update snippet (only specified fields)

**Path Parameters:**

- `id` (integer): The snippet ID

**Request Body:** (any of these fields)

```json
{
  "title": "string",
  "code": "string"
}
```

**Response:** `200 OK` (returns updated snippet object)

**Authentication:** Required (must be snippet owner)

---

#### 2.7 Delete Snippet

**Endpoint:** `DELETE /snippets/{id}/`

**Description:** Delete a code snippet

**Path Parameters:**

- `id` (integer): The snippet ID

**Response:** `204 No Content`

**Authentication:** Required (must be snippet owner)

**Example Request:**

```bash
curl -X DELETE http://localhost:8000/snippets/1/ \
  -H "Authorization: Bearer <token>"
```

---

### 3. Users Endpoints

#### 3.1 List All Users

**Endpoint:** `GET /users/`

**Description:** Get a paginated list of all users

**Query Parameters:**

- `page` (integer): Page number for pagination (default: 1)

**Response:** `200 OK`

```json
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [
    {
      "url": "http://localhost:8000/users/1/",
      "id": 1,
      "username": "john_doe"
    }
  ]
}
```

**Authentication:** Not required

---

#### 3.2 Retrieve User Details

**Endpoint:** `GET /users/{id}/`

**Description:** Get details of a specific user

**Path Parameters:**

- `id` (integer): The user ID

**Response:** `200 OK`

```json
{
  "url": "http://localhost:8000/users/1/",
  "id": 1,
  "username": "john_doe"
}
```

**Authentication:** Not required

---

### 4. API Root Endpoint

#### 4.1 API Entry Point

**Endpoint:** `GET /`

**Description:** API root endpoint providing links to main resources

**Response:** `200 OK`

```json
{
  "users": "http://localhost:8000/users/",
  "snippets": "http://localhost:8000/snippets/"
}
```

**Authentication:** Optional

---

### 5. API Documentation

#### 5.1 OpenAPI Schema

**Endpoint:** `GET /schema/`

**Description:** OpenAPI 3.0.3 schema for this API

**Query Parameters:**

- `format` (string): Response format (json, yaml)
- `lang` (string): Language code

**Response:** `200 OK` (OpenAPI schema)

**Authentication:** Optional

---

## Supported Languages

The API supports syntax highlighting for hundreds of programming languages. Here are the most common:

`python`, `javascript`, `java`, `c`, `cpp`, `csharp`, `php`, `ruby`, `go`, `rust`, `typescript`, `sql`, `html`, `css`, `json`, `xml`, `yaml`, `bash`, `powershell`, `swift`, `kotlin`, `scala`, `perl`, `lua`, `r`, `matlab`, `julia`, and many more...

---

## Supported Styles

Code highlighting styles available:

`default`, `friendly`, `monokai`, `vim`, `vs`, `autumn`, `borland`, `bw`, `colorful`, `emacs`, `fruity`, `gnuplot`, `igor`, `lovelace`, `manni`, `murphy`, `native`, `pastie`, `perldoc`, `rrt`, `solarized-dark`, `solarized-light`, `tango`, `trac`, `xcode`

---

## Error Responses

### Common Error Responses

**400 Bad Request**

```json
{
  "field_name": ["Error message"],
  "another_field": ["Error message"]
}
```

**401 Unauthorized**

```json
{
  "detail": "Authentication credentials were not provided."
}
```

**403 Forbidden**

```json
{
  "detail": "You do not have permission to perform this action."
}
```

**404 Not Found**

```json
{
  "detail": "Not found."
}
```

**500 Internal Server Error**

```json
{
  "detail": "Internal server error occurred."
}
```

---

## Rate Limiting

Currently, there are no rate limits implemented. Rate limiting may be added in future versions.

---

## CORS Headers

CORS is not enabled by default. Configure `CORS_ALLOWED_ORIGINS` in Django settings if frontend is on different domain.

---

## Example Frontend Workflows

### 1. User Registration & Login Flow

```
1. POST /api/auth/registration/ → Create account
2. POST /api/auth/login/ → Get JWT tokens (auto-stored in cookies)
3. GET /api/auth/user/ → Verify logged-in user
4. (Cookies automatically sent with subsequent requests)
```

### 2. Create and List Snippets

```
1. POST /api/auth/login/ → Authenticate
2. POST /snippets/ → Create new snippet
3. GET /snippets/ → List all snippets
4. GET /snippets/{id}/ → Get specific snippet
5. GET /snippets/{id}/highlight/ → Get highlighted HTML
```

### 3. Update Snippet

```
1. POST /api/auth/login/ → Authenticate
2. PATCH /snippets/{id}/ → Update snippet (partial)
   OR
   PUT /snippets/{id}/ → Update snippet (full)
3. GET /snippets/{id}/ → Verify update
```

### 4. Delete Snippet

```
1. POST /api/auth/login/ → Authenticate
2. DELETE /snippets/{id}/ → Delete snippet
3. GET /snippets/ → Verify deletion
```

### 5. Password Management

```
1. POST /api/auth/password/reset/ → Request reset
2. Check email for reset link
3. POST /api/auth/password/reset/confirm/ → Confirm new password
4. POST /api/auth/login/ → Login with new password
```

---

## HTTP Methods Supported

| Method | Purpose                        | Authentication   |
| ------ | ------------------------------ | ---------------- |
| GET    | Retrieve data                  | Optional         |
| POST   | Create data or perform actions | Usually Required |
| PUT    | Full resource update           | Required         |
| PATCH  | Partial resource update        | Required         |
| DELETE | Remove resource                | Required         |

---

## Headers

### Required Headers

- `Content-Type: application/json` (for POST, PUT, PATCH requests)

### Optional Headers

- `Authorization: Bearer <jwt_token>` (alternative to cookie authentication)

### Response Headers

- `X-Total-Count`: Total number of resources (in paginated responses)

---

## Pagination

List endpoints use page-based pagination with default page size of 10 items.

**Query Parameter:**

- `page=N` - Returns page N

**Response includes pagination metadata:**

```json
{
  "count": 42,
  "next": "http://localhost:8000/endpoint/?page=2",
  "previous": "http://localhost:8000/endpoint/?page=1",
  "results": [...]
}
```

---

## Status Codes

| Code | Meaning                                      |
| ---- | -------------------------------------------- |
| 200  | OK - Success                                 |
| 201  | Created - Resource created successfully      |
| 204  | No Content - Success with no response body   |
| 400  | Bad Request - Invalid parameters             |
| 401  | Unauthorized - Authentication required       |
| 403  | Forbidden - Not authorized for this resource |
| 404  | Not Found - Resource doesn't exist           |
| 500  | Internal Server Error - Server error         |

---

## Terms and Definitions

- **JWT**: JSON Web Token - A secure token used for authentication
- **Access Token**: Short-lived token used for API requests
- **Refresh Token**: Long-lived token used to obtain new access tokens
- **Snippet**: A code snippet stored in the database
- **Language**: Programming language of the code (e.g., python, javascript)
- **Style**: Syntax highlighting color scheme
- **Owner**: User who created the snippet
- **Linenos**: Whether to display line numbers in highlighted output

---

## Frontend Implementation Notes

1. **Token Storage**: Tokens are automatically stored in HTTP-only cookies after login. No manual token management needed in most cases.

2. **CSRF Protection**: If making requests from a form, include CSRF token in headers.

3. **Pagination**: Always check the `next` and `previous` fields for navigation.

4. **Error Handling**: Always check for error responses and display appropriate messages to users.

5. **Snippet Creation**: The `highlighted` field will contain pre-rendered HTML. Display this instead of rendering the raw code.

6. **Permissions**: Only snippet owners can edit/delete their snippets. The API will return 403 Forbidden otherwise.

7. **Email Verification**: Email verification is currently set to "none", but verify email endpoints are available for future use.
