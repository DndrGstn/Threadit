# Threadit – A Reddit-Style Forum

A full-stack forum web application built with Django and SQLite. Users can sign up, create communities, post threads, comment, reply, search, and manage their own content.

---

## Features

- User registration and login/logout
- Create and browse communities (like subreddits)
- Create, edit, and delete posts
- Comment on posts with nested replies
- Search posts by keyword
- Fully responsive layout
- Admin panel for site management

---

## Tech Stack

| Layer     | Technology            |
|-----------|-----------------------|
| Backend   | Python 3 / Django     |
| Database  | SQLite (via Django ORM)|
| Frontend  | HTML5, CSS3, vanilla JS |
| Auth      | Django built-in auth  |

---

## Local Setup

### 1. Clone the project

```bash
git clone <your-repo-url>
cd forumsite
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install django
```

### 4. Apply database migrations

```bash
python manage.py migrate
```

### 5. (Optional) Load demo data

```bash
python manage.py shell < seed.py
```

### 6. Create a superuser (for admin panel)

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000

Admin panel: http://127.0.0.1:8000/admin

---

## Running Tests

```bash
python manage.py test forum
```

18 automated tests cover:
- Model methods and relationships
- Page response codes
- Authentication (login, register, logout)
- Authorization (only authors can edit/delete their posts)
- Full CRUD operations (create, read, update, delete posts)
- Search functionality

---

## File Structure

```
forumsite/
├── forum/                  # Main app
│   ├── migrations/         # Database migration files
│   ├── admin.py            # Admin panel config
│   ├── forms.py            # Django forms
│   ├── models.py           # Database models
│   ├── tests.py            # Automated tests
│   ├── urls.py             # App URL routes
│   └── views.py            # View logic
├── forumsite/              # Project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── static/css/style.css    # Custom stylesheet
├── templates/forum/        # HTML templates
├── db.sqlite3              # SQLite database (auto-created)
├── manage.py
└── README.md
```

---

## Database Design

Three main models with relationships:

```
User (built-in Django)
  |
  ├── Community (created_by → User)
  |
  ├── Post (author → User, community → Community)
  |
  └── Comment (author → User, post → Post, parent → Comment)
```

- **Community** – A named topic space; belongs to a creator.
- **Post** – Belongs to a Community and an author; can have many Comments.
- **Comment** – Belongs to a Post and an author; optionally belongs to a parent Comment (for replies).

---

## Deployment (Heroku)

1. Add `gunicorn` and `whitenoise` to dependencies
2. Create a `Procfile`:
   ```
   web: gunicorn forumsite.wsgi
   ```
3. Set `DEBUG = False` and configure `ALLOWED_HOSTS` with your Heroku domain
4. Add `whitenoise` middleware for static files
5. Push to Heroku:
   ```bash
   heroku create
   git push heroku main
   heroku run python manage.py migrate
   ```

---

## Accessibility

- Semantic HTML elements (`nav`, `main`, `aside`)
- ARIA-friendly form labels
- Sufficient colour contrast ratios
- Keyboard-navigable interface
- Responsive layout works on mobile and desktop
