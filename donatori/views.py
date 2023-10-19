import csv
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib import messages
from .models import donatori as mDonatori


@login_required
def donatori(request):
    if request.user.is_staff:
        lDonatori = mDonatori.objects.all().order_by('-tessera')
        paginator = Paginator(lDonatori, 50)
        page_number = request.GET.get("p")
        page_obj = paginator.get_page(page_number)
        return render(request, "donatori.html", {'page_obj': page_obj})
    else:
        return redirect("/")


@login_required
def elimina(request):
    if request.user.is_staff:
        tesseraCanc = request.POST.get('tesseraCanc')
        lDonatori = mDonatori.objects.get(tessera=tesseraCanc)
        u = User.objects.get(username=lDonatori.email)
        u.delete()
        lDonatori = mDonatori.objects.filter(tessera=tesseraCanc).delete()
        messages.success(request, "Scheda donatore eliminata con successo!")
        return redirect('donatori')
    else:
        return redirect("/")


@login_required
def modifica(request):
    if request.user.is_staff:
        tesseraMod = request.POST.get('tesseraMod')
        if not mDonatori.objects.filter(tessera=tesseraMod).exists():
            messages.warning(request, "Errore: Numero tessera non valido!")
            return redirect('donatori')
        else:
            lDonatori = mDonatori.objects.get(tessera=tesseraMod)
            return render(request, "modifica.html", {'donatore': lDonatori})
    else:
        return redirect("/")


@login_required
def aggiungi(request):
    if request.user.is_staff:
        upassword = get_random_string(length=16)
        email = request.POST.get('email')
        User.objects.create_user(username=email, email=email, password=upassword)
        lDonatori = mDonatori.objects.create()

        if 'fototessera' in request.FILES:
            fototesseraI = request.FILES["fototessera"]
            lDonatori.fototessera = InMemoryUploadedFile(fototesseraI, None, str(lDonatori.tessera) + fototesseraI.name, fototesseraI.file, fototesseraI.size, fototesseraI.charset)

        lDonatori.dataiscrizione = request.POST.get('dataiscrizione')
        lDonatori.grupposang = request.POST.get('grupposanguigno')
        lDonatori.fenotipo = request.POST.get('fenotipo')
        lDonatori.kell = request.POST.get('kell')
        lDonatori.nome = request.POST.get('nome')
        lDonatori.cognome = request.POST.get('cognome')
        lDonatori.datadinascita = request.POST.get('datadinascita')
        lDonatori.luogodinascita = request.POST.get('luogodinascita')
        lDonatori.codicefiscale = (request.POST.get('codicefiscale')).upper()
        lDonatori.indirizzo = request.POST.get('indirizzo')
        lDonatori.comune = request.POST.get('comune')
        lDonatori.tel = request.POST.get('telefono')
        lDonatori.email = email
        lDonatori.save()
        set_password_form = PasswordResetForm({'email': email})
        if set_password_form.is_valid():
            set_password_form.save(request=request, use_https=False, html_email_template_name='pw_reset_email.html', subject_template_name="pw_reset_email_subjet.txt")

        messages.success(request, "Scheda donatore aggiunta con successo!")
        return redirect('donatori')
    else:
        return redirect("/")


@login_required
def salva(request):
    if request.user.is_staff:
        tesseraMod = request.POST.get('tesseraMod')
        lDonatori = mDonatori.objects.get(tessera=tesseraMod)

        if 'fototessera' in request.FILES:
            fototesseraI = request.FILES["fototessera"]
            lDonatori.fototessera = InMemoryUploadedFile(fototesseraI, None, str(lDonatori.tessera) + fototesseraI.name, fototesseraI.file, fototesseraI.size, fototesseraI.charset)

        lDonatori.dataiscrizione = request.POST.get('dataiscrizione')
        lDonatori.grupposang = request.POST.get('grupposanguigno')
        lDonatori.fenotipo = request.POST.get('fenotipo')
        lDonatori.kell = request.POST.get('kell')
        lDonatori.nome = request.POST.get('nome')
        lDonatori.cognome = request.POST.get('cognome')
        lDonatori.datadinascita = request.POST.get('datadinascita')
        lDonatori.luogodinascita = request.POST.get('luogodinascita')
        lDonatori.codicefiscale = (request.POST.get('codicefiscale')).upper()
        lDonatori.indirizzo = request.POST.get('indirizzo')
        lDonatori.comune = request.POST.get('comune')
        lDonatori.tel = request.POST.get('telefono')
        lDonatori.email = request.POST.get('email')
        lDonatori.save()
        messages.success(request, "Scheda donatore salvata con successo!")
        return redirect('donatori')
    else:
        return redirect("/")


@login_required
def esporta(request):
    if request.user.is_staff:
        response = HttpResponse(content_type="text/csv", headers={"Content-Disposition": 'attachment; filename="donatori.csv"'})
        lDonatori = mDonatori.objects.all()
        writer = csv.writer(response)
        writer.writerow(["tessera", "dataiscrizione", "grupposang", "fenotipo", "kell", "nome", "cognome", "datadinascita", "luogodinascita", "codicefiscale", "indirizzo", "comune", "tel", "email"])
        for x in lDonatori:
            writer.writerow([x.tessera, x.dataiscrizione, x.grupposang, x.fenotipo, x.kell, x.nome, x.cognome, x.datadinascita, x.luogodinascita, x.codicefiscale, x.indirizzo, x.comune, x.tel, x.email])

        return response
    else:
        return redirect("/")
