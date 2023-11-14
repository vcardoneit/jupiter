import csv
import os
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from donatori.models import donatori as mDonatori
from django.shortcuts import get_object_or_404
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from datetime import datetime
from .models import donazioni as mDonazioni


@login_required
def salva(request):
    if request.user.is_staff:
        donazioneMod = request.POST.get('donazioneMod')
        lDonazioni = mDonazioni.objects.get(id=donazioneMod)
        lDonazioni.donatore = mDonatori.objects.get(pk=request.POST.get('tessera'))
        lDonazioni.data = datetime.strptime(request.POST.get('data'), '%Y-%m-%d')
        lDonazioni.tipo = request.POST.get('tipodonazione')

        if 'referto' in request.FILES:
            referto = request.FILES["referto"]
            lDonazioni.referto = InMemoryUploadedFile(referto, None, "Referto " + lDonazioni.donatore.nome + " " + lDonazioni.donatore.cognome + " " + request.POST.get('data') + ".pdf", referto.file, referto.size, referto.charset)

            html_message = render_to_string("referto.html", {'donazione': lDonazioni})
            plain_message = strip_tags(html_message)

            message = EmailMultiAlternatives(
                subject="Referto dell'esame relativo alla donazione ora disponibile!",
                body=plain_message,
                from_email=os.getenv("DEFAULT_FROM_EMAIL"),
                to=[lDonazioni.donatore.email]
            )

            message.attach_alternative(html_message, "text/html")
            message.send()

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


@login_required
def download(request, dId):
    if request.user.is_staff:
        donazione = get_object_or_404(mDonazioni, id=dId)
        donatore = get_object_or_404(mDonatori, tessera=donazione.donatore.tessera)
        try:
            response = HttpResponse(donazione.referto.file, content_type='application/octet-stream')
            response['Content-Disposition'] = 'attachment; filename={}'.format("Referto " + donatore.nome + " " + donatore.cognome + " " + donazione.data.strftime("%d-%m-%Y") + ".pdf")
            return response
        except Exception:
            messages.warning(request, "File non trovato, potrebbe essere scaduto o non disponibile.")
            return redirect("donazioni")
    else:
        donatore = get_object_or_404(mDonatori, email=request.user.email)
        donazione = get_object_or_404(mDonazioni, id=dId)
        if (donazione.donatore.tessera & donatore.tessera):
            try:
                response = HttpResponse(donazione.referto.file, content_type='application/octet-stream')
                response['Content-Disposition'] = 'attachment; filename={}'.format("Referto " + donatore.nome + " " + donatore.cognome + " " + donazione.data.strftime("%d-%m-%Y") + ".pdf")
                return response
            except Exception:
                messages.warning(request, "File non trovato, potrebbe essere scaduto o non disponibile.")
                return redirect("donazioni")
        else:
            messages.warning(request, "Non hai il permesso per accedere a questo file!")
            return redirect("donazioni")
