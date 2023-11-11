from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from donazioni.models import donazioni
from donatori.models import donatori
from django.db.models import Q
from datetime import datetime


@login_required
def statistiche(request):
    if request.user.is_staff:
        stats = {}
        stats['totaleDonatori'] = donatori.objects.all().count()
        stats['totaleDonazioni'] = donazioni.objects.all().count()
        stats['donazioniSangue'] = donazioni.objects.filter(tipo="Sangue").count()
        stats['donazioniPlasma'] = donazioni.objects.filter(tipo="Plasma").count()
        stats['donazioniPiastrine'] = donazioni.objects.filter(tipo="Piastrine").count()

        stats['mlSangue'] = donazioni.objects.filter(tipo="Sangue").count() * 450
        stats['mlPlasma'] = donazioni.objects.filter(tipo="Plasma").count() * 450

        return render(request, "statistiche.html", {'stats': stats})
    else:
        return redirect("/")


@login_required
def ricerca(request):
    if request.user.is_staff:
        dataInizio = request.POST.get("dataInizio")
        dataFine = request.POST.get("dataFine")

        statsRs = {}
        statsRs['dataInizio'] = datetime.strptime(dataInizio, '%Y-%m-%d')
        statsRs['dataFine'] = datetime.strptime(dataFine, '%Y-%m-%d')

        statsRs['totaleDonatori'] = donatori.objects.filter(Q(dataiscrizione__gte=dataInizio) & Q(dataiscrizione__lte=dataFine)).count()
        statsRs['totaleDonazioni'] = donazioni.objects.filter(Q(data__gte=dataInizio) & Q(data__lte=dataFine)).count()
        statsRs['donazioniSangue'] = donazioni.objects.filter(Q(data__gte=dataInizio) & Q(data__lte=dataFine) & Q(tipo="Sangue")).count()
        statsRs['donazioniPlasma'] = donazioni.objects.filter(Q(data__gte=dataInizio) & Q(data__lte=dataFine) & Q(tipo="Plasma")).count()
        statsRs['donazioniPiastrine'] = donazioni.objects.filter(Q(data__gte=dataInizio) & Q(data__lte=dataFine) & Q(tipo="Piastrine")).count()

        statsRs['mlSangue'] = donazioni.objects.filter(Q(data__gte=dataInizio) & Q(data__lte=dataFine) & Q(tipo="Sangue")).count() * 450
        statsRs['mlPlasma'] = donazioni.objects.filter(Q(data__gte=dataInizio) & Q(data__lte=dataFine) & Q(tipo="Plasma")).count() * 450

        return render(request, "statistiche.html", {'statsRs': statsRs})
    else:
        return redirect("/")
