import csv
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from donatori.models import donatori as mDonatori
from .models import donazioni as mDonazioni


@login_required
def salva(request):
    if request.user.is_staff:
        donazioneMod = request.POST.get('donazioneMod')
        lDonazioni = mDonazioni.objects.get(id=donazioneMod)
        lDonazioni.donatore = mDonatori.objects.get(pk=request.POST.get('tessera'))
        lDonazioni.data = request.POST.get('data')
        lDonazioni.tipo = request.POST.get('tipodonazione')
        lDonazioni.save()
        messages.success(request, "Scheda donazione salvata con successo!")
        return redirect('donazioni')
    return ("/")


@login_required
def donazioni(request):
    if request.user.is_staff:
        if request.method == 'POST' and 'donazioneCanc' in request.POST:
            idDonazione = request.POST.get('donazioneCanc')
            lDonazioni = mDonazioni.objects.filter(id=idDonazione).delete()
            messages.success(request, "Scheda donazione eliminata con successo!")
            return redirect('donazioni')
        else:
            lDonazioni = mDonazioni.objects.all()
            return render(request, "donazioni.html", {'donazioni': lDonazioni})
    else:
        lDonazioni = mDonazioni.objects.filter(donatore__email=request.user.email)
        return render(request, "donazioni.html", {'donazioni': lDonazioni})


@login_required
def modifica(request):
    if request.user.is_staff:
        donazioneMod = request.POST.get('donazioneMod')

        if not mDonazioni.objects.filter(id=donazioneMod).exists():
            messages.warning(request, "Errore: ID Donazione non valido!")
            return redirect('donazioni')
        else:
            lDonazioni = mDonazioni.objects.get(id=donazioneMod)
            return render(request, "modificaDonazione.html", {'donazione': lDonazioni})
    else:
        return redirect("/")


@login_required
def aggiungi(request):
    if request.user.is_staff:
        if not mDonatori.objects.filter(pk=request.POST.get('tessera')).exists():
            messages.warning(request, "Errore: Numero tessera non valido!")
            return redirect('donazioni')
        else:
            lDonazioni = mDonazioni.objects.create(donatore_id=request.POST.get('tessera'))
            lDonazioni.data = request.POST.get('datadonazione')
            lDonazioni.tipo = request.POST.get('tipodonazione')
            lDonazioni.save()

            return redirect("donazioni")
    else:
        return redirect("/")


@login_required
def storico(request):
    if request.user.is_staff:
        if not mDonatori.objects.filter(pk=request.POST.get('visualDonazioni')).exists():
            messages.warning(request, "Errore: Numero tessera non valido!")
            return redirect('donazioni')
        else:
            numeroTessera = request.POST.get('visualDonazioni')
            lDonazioni = mDonazioni.objects.all().filter(donatore_id=numeroTessera)
            return render(request, "storicoDonazioni.html", {'donazioni': lDonazioni, "tessera": numeroTessera})
    else:
        return redirect("/")


@login_required
def esporta(request):
    if request.user.is_staff:
        response = HttpResponse(content_type="text/csv", headers={"Content-Disposition": 'attachment; filename="donazioni.csv"'})
        lDonazioni = mDonazioni.objects.all()
        writer = csv.writer(response)
        writer.writerow(["id", "donatore", "data", "tipo"])
        for x in lDonazioni:
            writer.writerow([x.id, x.donatore_id, x.data, x.tipo])

        return response
    else:
        return ("/")
