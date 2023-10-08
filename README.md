<h1 align="center">Jupiter</h1>
<p align="center">Jupiter è una web app per la gestione delle attività riguardanti la donazione del sangue utilizzata dalla Croce Rossa Italiana di Avola

## Features
- **Gestione Donatori**
- **Gestione Donazioni**
- **Statistiche**
- **Invio appello a tutti i Donatori**
- **Accesso Donatore**
- **Esporta i dati in CSV**
- **Molto altro..**

## Build
```
docker compose -f docker-compose.yml up -d --build
docker compose -f docker-compose.yml exec web python manage.py migrate --noinput
```

## Environment Variables (web)
| Environment Variable  |
| ------------- |
| `DEBUG` |
| `SECRET_KEY` |
| `SQL_ENGINE` |
| `SQL_DATABASE` |
| `SQL_USER` |
| `SQL_PASSWORD` |
| `SQL_HOST` |
| `SQL_PORT` |
| `DJANGO_ALLOWED_HOSTS` |
| `CSRF_TRUSTED_ORIGINS` |
| `EMAIL_HOST` |
| `EMAIL_HOST_USER` |
| `EMAIL_HOST_PASSWORD` |
| `SESSION_COOKIE_SECURE` |
| `CSRF_COOKIE_SECURE` |

## Environment Variables (db)
| Environment Variable  |
| ------------- |
| `POSTGRES_USER` |
| `POSTGRES_PASSWORD` |
| `POSTGRES_DB` |

## Problems / Questions
<b>Email:</b> jupiter@vcardone.it
