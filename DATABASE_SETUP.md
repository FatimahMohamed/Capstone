# Database Configuration Guide

## Development (SQLite)
For local development, we use SQLite which is simple and doesn't require any additional setup.

## Production (PostgreSQL)
For Heroku deployment, we use PostgreSQL. The database URL is stored in environment variables.

## Switching Between Databases

### To use SQLite (Development):
Comment out the DATABASE_URL line in env.py:
```python
# os.environ['DATABASE_URL'] = 'postgresql://...'
```

### To use PostgreSQL (Production):
Uncomment the DATABASE_URL line in env.py:
```python
os.environ['DATABASE_URL'] = 'postgresql://...'
```

## Database Commands

### Run migrations:
```bash
python manage.py migrate
```

### Create superuser:
```bash
python manage.py createsuperuser
```

### Access admin panel:
http://127.0.0.1:8000/admin/
Username: admin
Password: admin123
