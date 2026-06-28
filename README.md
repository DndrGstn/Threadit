# Threadit – A Reddit-Style Forum

## Overview

Threadit is a full-stack Reddit-style discussion forum built with Django. Users can create an account, browse communities, create posts, leave comments and replies, and search for content. The application implements full CRUD functionality while demonstrating user authentication, database relationships, responsive design, and secure deployment.

---

# Features

- User registration and authentication
- Login and logout functionality
- Create and browse communities
- Create, edit and delete posts
- Nested comments and replies
- Search posts by keyword
- Responsive design for desktop and mobile
- Django administration panel

---

# Technologies Used

| Layer | Technology |
|--------|------------|
| Backend | Python 3, Django |
| Database | SQLite (Django ORM) |
| Frontend | HTML5, CSS3, JavaScript |
| Authentication | Django Authentication System |
| Deployment | Heroku |
| Static Files | WhiteNoise |
| Web Server | Gunicorn |

---

# Database Design

The application contains three primary models related to Django's built-in User model.

```
User
│
├── Community
│     └── created_by
│
├── Post
│     ├── author
│     └── community
│
└── Comment
      ├── author
      ├── post
      └── parent (self relationship)
```

### Community

Stores discussion communities created by registered users.

### Post

Belongs to a Community and a User.

### Comment

Belongs to a Post and optionally another Comment to support nested replies.

---

# Installation

## Clone Repository

```bash
git clone <repository-url>
cd forumsite
```

## Create Virtual Environment

```bash
python -m venv venv
```

Windows

```bash
venv\Scripts\activate
```

Mac/Linux

```bash
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run Migrations

```bash
python manage.py migrate
```

## Create Superuser

```bash
python manage.py createsuperuser
```

## Start Development Server

```bash
python manage.py runserver
```

Open

```
http://127.0.0.1:8000
```

Admin

```
http://127.0.0.1:8000/admin
```

---

# Testing

## Automated Testing

The application includes 18 automated tests using Django's built-in testing framework.

Tests cover:

- Model relationships
- CRUD functionality
- Authentication
- Authorization
- Page response codes
- Search functionality

Tests are executed using:

```bash
python manage.py test forum
```

The project includes 18 automated tests covering the functionality listed above.

---

## Manual Testing

The following manual tests were performed on the deployed application.

| Feature | Expected Result | Result |
|---------|-----------------|--------|
| User Registration | User account created successfully | ✅ Pass |
| Login | User redirected after login | ✅ Pass |
| Logout | User session ended successfully | ✅ Pass |
| Create Community | Community created | ✅ Pass |
| Create Post | Post displayed correctly | ✅ Pass |
| Edit Post | Changes saved | ✅ Pass |
| Delete Post | Post removed | ✅ Pass |
| Create Comment | Comment displayed | ✅ Pass |
| Reply to Comment | Nested reply displayed | ✅ Pass |
| Search | Relevant posts returned | ✅ Pass |
| Heroku Deployment | Application loads correctly after deployment | ✅ Pass |
| Production 404 Test | Invalid URL returns production 404 without Django traceback | ✅ Pass |

---

# Validation

The project was validated using several industry-standard tools. Screenshots of the validation results are included below.

## HTML

Validated using the W3C HTML Validator.

**Result:** No errors or warnings.

<img width="1911" height="946" alt="Screenshot 2026-06-28 224958" src="https://github.com/user-attachments/assets/45fa882e-afae-409a-b553-19f72b4b4538" />

---

## CSS

Validated using the W3C CSS Validator.

**Result:** No errors.

<img width="1913" height="948" alt="Screenshot 2026-06-28 224819" src="https://github.com/user-attachments/assets/40b5ccd8-b389-4d26-bf11-f71a01929e3c" />

---

## Lighthouse

Google Lighthouse audit results:

| Category | Score |
|-----------|------:|
| Performance | 100 |
| Accessibility | 93 |
| Best Practices | 100 |
| SEO | 90 |

<img width="583" height="949" alt="Screenshot 2026-06-28 225107" src="https://github.com/user-attachments/assets/0c219aeb-d61d-4e4f-a998-a15cd4714b06" />

---

## Production Security

Following the previous assessment feedback, the production deployment was reviewed and updated to ensure secure configuration.

The following improvements were implemented:

- DEBUG disabled in production
- SECRET_KEY stored securely using Heroku Config Vars
- ALLOWED_HOSTS configured correctly for the deployed application

An invalid URL was tested to verify that Django no longer exposes debug tracebacks in production. The application correctly returns a standard production 404 page.

---

# Accessibility

The application includes:

- Semantic HTML elements
- Accessible form labels
- Keyboard navigation
- Responsive layouts
- Colour contrast suitable for readability

---

# File Structure

```
forumsite/
├── forum/
│   ├── migrations/
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── forumsite/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── templates/
├── static/
├── manage.py
└── README.md
```

---

# Deployment (Heroku)

1. Create a Heroku application.
2. Add Config Vars including:

- SECRET_KEY
- DATABASE_URL

3. Install:

- gunicorn
- whitenoise

4. Create a Procfile

```
web: gunicorn forumsite.wsgi
```

5. Configure:

- DEBUG=False
- ALLOWED_HOSTS
- WhiteNoise

6. Push to Heroku.

```bash
git push heroku main
```

7. Apply migrations.

```bash
heroku run python manage.py migrate
```

---

# Future Improvements

- User profile pages
- Upvote/downvote system
- Notifications
- Rich text editor
- Improved search functionality

---

# Credits

Built using:

- Django Documentation
- MDN Web Docs
- W3Schools
- Heroku Documentation
