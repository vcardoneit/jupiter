from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from django.contrib import messages
from .serializers import prenotazioniSer
from .models import prenotazioni
from idoneita.models import idoneita as lidoneita
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from .utils import notificaPrenotazioni


class addprt(APIView):
    permission_classes = [HasAPIKey]
    renderer_classes = [JSONRenderer]

    def post(self, request, format=None):
        serializer = prenotazioniSer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@login_required
def index(request):
    if request.user.is_staff:
        lprenotazioni = prenotazioni.objects.all()
        return render(request, "prenotazioni.html", {'prenotazioni': lprenotazioni})
    else:
        return redirect("/")


@login_required
def conferma(request):
    if request.user.is_staff:
        prenotazione = request.POST.get('idPren')
        if not prenotazioni.objects.filter(id=prenotazione).exists():
            messages.warning(request, "Errore: ID non valido!")
            return redirect('prenotazioni')
        else:
            prenotazione = prenotazioni.objects.get(id=prenotazione)
            if (prenotazione.analisieffettuate == "Si"):

                idoneita = lidoneita.objects.create()
                idoneita.nominativo = prenotazione.nome
                idoneita.dataprelievo = prenotazione.data
                idoneita.telefono = prenotazione.telefono
                idoneita.save()

                prenotazione.delete()

                messages.success(request, "Pre-donazione confermata! L'utente è stato inserito nella lista delle predonazioni in attesa di idoneità!")
                return redirect('prenotazioni')
            else:
                prenotazione.delete()
                messages.success(request, "Prenotazione confermata! In quanto l'utente ha dichiarato di aver già donato in passato, non è stato inserito nella lista delle predonazioni!")
                return redirect('prenotazioni')
    else:
        return redirect("/")


@login_required
def elimina(request):
    if request.user.is_staff:
        prenotazione = request.POST.get('idPren')
        if not prenotazioni.objects.filter(id=prenotazione).exists():
            messages.warning(request, "Errore: ID non valido!")
            return redirect('prenotazioni')
        else:
            prenotazione = prenotazioni.objects.get(id=prenotazione)
            prenotazione.delete()
            messages.success(request, "Prenotazione eliminata con successo!")
            return redirect('prenotazioni')
    else:
        return redirect("/")


scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")


@register_job(scheduler, "cron", day_of_week="thu", hour=14, id="jobNotificaPrt", replace_existing=True)
def jobNotifica():
    notificaPrenotazioni()


register_events(scheduler)
scheduler.start()
