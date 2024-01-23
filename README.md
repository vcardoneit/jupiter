<h1 align="center">Jupiter</h1>
<p align="center">Jupiter è una web app per la gestione delle attività riguardanti la donazione del sangue utilizzata dalla Croce Rossa Italiana di Avola

## Wiki - Documentazione
Consulta la [wiki](https://github.com/vcardoneit/jupiter/wiki) per scoprire tutte le diverse funzionalità e come utilizzarle!

## Funzionalità
- **Gestione Donatori, Donazioni e Predonazioni**
- **Emissione tessera con verifica tramite QR**
- **Statistiche**
- **Invio appello a tutti i Donatori**
- **Accesso Donatore**
- **Gestione prenotazioni**
- **API per inserire prenotazione - /api/addprt/**
- **Esportazione dati in CSV**
- **Promemoria prenotazioni via e-mail**

## Installazione
#### Docker compose
Consulta la documentazione per maggiori dettagli
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

## Domande - Segnalazioni
<b>Email:</b> jupiter@vcardone.it
