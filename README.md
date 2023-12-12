<h1 align="center">Jupiter</h1>
<p align="center">Jupiter è una web app per la gestione delle attività riguardanti la donazione del sangue utilizzata dalla Croce Rossa Italiana di Avola

## Features
- **Gestione Donatori, Donazioni e Predonazioni**
- **Emissione tessera con verifica tramite QR**
- **Statistiche**
- **Invio appello a tutti i Donatori**
- **Accesso Donatore**
- **Gestione prenotazioni**
- **API per inserire prenotazione - /api/addprt/**
- **Esportazione dati in CSV**

## Installation with Docker
#### Docker compose
```yaml
version: "3.8"

services:
  web:
    image: 'ghcr.io/vcardoneit/jupiter-web:latest'
    command: gunicorn jupiter.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - static_volume:/home/jupiter/web/staticfiles
    expose:
      - 8000
    env_file:
      - stack.env
    depends_on:
      - db
  db:
    image: 'postgres:15'
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    env_file:
      - stack.env
  nginx:
    image: 'ghcr.io/vcardoneit/jupiter-nginx:latest'
    volumes:
      - static_volume:/home/jupiter/web/staticfiles
      - certs:/home/jupiter/ssl
    ports:
      - 1642:443
    depends_on:
      - web

volumes:
  postgres_data:
  static_volume:
  certs:
```

#### Environment Variables
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
| `DEFAULT_FROM_EMAIL` |
| `SESSION_COOKIE_SECURE` |
| `CSRF_COOKIE_SECURE` |
| `POSTGRES_USER` |
| `POSTGRES_PASSWORD` |
| `POSTGRES_DB` |

## Problems / Questions
<b>Email:</b> jupiter@vcardone.it

## Screenshot
<p align="center"><img src="https://i.imgur.com/qSCCRDQ.png"></p>
<p align="center"><img src="https://i.imgur.com/DEfwXzI.png"></p>
<p align="center"><img src="https://i.imgur.com/AfWo6JU.png"></p>
<p align="center"><img src="https://i.imgur.com/gngm488.png"></p>
