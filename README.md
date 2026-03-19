# PDF Library Website

A Django-based PDF sharing website where admins upload PDFs and visitors can browse, search, preview, download, and share them.

## Features

- Admin-only PDF uploads through Django admin
- Auto title generation from uploaded file names
- Category-wise organization
- Search by title or category
- In-browser PDF preview
- Download and share actions
- SQLite database and local `media/` storage
- Render deployment config included

## Project Structure

- `pdfsite/` - Django project settings and root URLs
- `app/` - Models, views, templates, admin, tests, and app URLs
- `media/` - Uploaded PDFs
- `manage.py` - Django management entry point

## Local Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/admin/` to upload PDFs.

## Render Deployment

The included `render.yaml` deploys the Django app with Gunicorn.

Before production deployment, update these settings as needed:

- Set a secure `SECRET_KEY`
- Set `DEBUG = False`
- Restrict `ALLOWED_HOSTS`
- Configure persistent media storage if required
