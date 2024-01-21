import os
from datetime import datetime, timedelta
from django.core.mail import EmailMessage
from .models import prenotazioni


def notificaPrenotazioni():
    gg = datetime.now() + timedelta(days=1)
    dbListaPrenotazioni = prenotazioni.objects.filter(data=gg.date())

    if not dbListaPrenotazioni:
        return

    listaPrenotazioni = "<br>".join([f"<b>Nome:</b> {prenotazione.nome} - <b>Telefono:</b> {prenotazione.nome} - <b>Ha effettuato le analisi predonazione:</b> {prenotazione.analisieffettuate}" for prenotazione in dbListaPrenotazioni])

    oggetto = "Prenotazioni donazione sangue " + gg.strftime("%d/%m/%Y")

    corpo = f'Prenotazioni per la donazione del sangue di domani: <br><br>{listaPrenotazioni}'

    notifyemail = os.environ.get('NOTIFYEMAIL', '')

    if notifyemail:
        listaEmail = notifyemail.split(',')
    else:
        listaEmail = []

    email = EmailMessage(
        oggetto,
        corpo,
        os.getenv("DEFAULT_FROM_EMAIL"),
        listaEmail,
    )
    email.content_subtype = "html"
    email.send()
