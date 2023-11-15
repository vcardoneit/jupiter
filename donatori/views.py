import csv
import os
import qrcode
from jupiter.settings import BASE_DIR
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib import messages
from django.conf import settings
from .models import donatori as mDonatori
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO


@login_required
def donatori(request):
    if request.user.is_staff:
        lDonatori = mDonatori.objects.all()
        return render(request, "donatori.html", {'donatori': lDonatori})
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
        try:
            User.objects.create_user(username=email, email=email, password=upassword)
        except Exception:
            messages.warning(request, "Utente non creato, esista già un utente con questa email!")
            return redirect("donatori")
        lDonatori = mDonatori.objects.create()

        if 'fototessera' in request.FILES:
            fototesseraI = request.FILES["fototessera"]
            lDonatori.fototessera = InMemoryUploadedFile(fototesseraI, None, str(lDonatori.tessera) + fototesseraI.name, fototesseraI.file, fototesseraI.size, fototesseraI.charset)

        lDonatori.dataiscrizione = request.POST.get('dataiscrizione')
        lDonatori.grupposang = request.POST.get('grupposanguigno')
        lDonatori.nome = request.POST.get('nome')
        lDonatori.cognome = request.POST.get('cognome')
        lDonatori.datadinascita = request.POST.get('datadinascita')
        lDonatori.luogodinascita = request.POST.get('luogodinascita')
        lDonatori.codicefiscale = (request.POST.get('codicefiscale')).upper()
        lDonatori.indirizzo = request.POST.get('indirizzo')
        lDonatori.comune = request.POST.get('comune')
        lDonatori.tel = request.POST.get('telefono')
        lDonatori.email = email
        lDonatori.modReferti = request.POST.get('modref')

        if 'privacy_a' in request.POST:
            lDonatori.privacy_a = request.POST.get('privacy_a')
        if 'privacy_b' in request.POST:
            lDonatori.privacy_b = request.POST.get('privacy_b')
        if 'privacy_c' in request.POST:
            lDonatori.privacy_c = request.POST.get('privacy_c')

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
            if str(lDonatori.fototessera) != "default.jpg":
                os.remove(os.path.join(settings.MEDIA_ROOT, str(lDonatori.fototessera)))
            lDonatori.fototessera = InMemoryUploadedFile(fototesseraI, None, str(lDonatori.tessera) + fototesseraI.name, fototesseraI.file, fototesseraI.size, fototesseraI.charset)

        lDonatori.dataiscrizione = request.POST.get('dataiscrizione')
        lDonatori.grupposang = request.POST.get('grupposanguigno')
        lDonatori.nome = request.POST.get('nome')
        lDonatori.cognome = request.POST.get('cognome')
        lDonatori.datadinascita = request.POST.get('datadinascita')
        lDonatori.luogodinascita = request.POST.get('luogodinascita')
        lDonatori.codicefiscale = (request.POST.get('codicefiscale')).upper()
        lDonatori.indirizzo = request.POST.get('indirizzo')
        lDonatori.comune = request.POST.get('comune')
        lDonatori.tel = request.POST.get('telefono')
        lDonatori.email = request.POST.get('email')
        lDonatori.modReferti = request.POST.get('modref')

        if 'privacy_a' in request.POST:
            lDonatori.privacy_a = request.POST.get('privacy_a')
        else:
            lDonatori.privacy_a = False

        if 'privacy_b' in request.POST:
            lDonatori.privacy_b = request.POST.get('privacy_b')
        else:
            lDonatori.privacy_b = False

        if 'privacy_c' in request.POST:
            lDonatori.privacy_c = request.POST.get('privacy_c')
        else:
            lDonatori.privacy_c = False

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
        writer.writerow(["tessera", "dataiscrizione", "grupposang", "nome", "cognome", "datadinascita", "luogodinascita", "codicefiscale", "indirizzo", "comune", "tel", "email"])
        for x in lDonatori:
            writer.writerow([x.tessera, x.dataiscrizione, x.grupposang, x.nome, x.cognome, x.datadinascita, x.luogodinascita, x.codicefiscale, x.indirizzo, x.comune, x.tel, x.email])

        return response
    else:
        return redirect("/")


@login_required
def scaricaTessera(request):
    if request.user.is_staff:
        numTessera = request.POST.get("numTessera")
        if not mDonatori.objects.filter(tessera=numTessera).exists():
            messages.warning(request, "Errore: Numero tessera non valido!")
            return redirect('donatori')
        else:
            donatore = mDonatori.objects.get(tessera=numTessera)

            img = Image.open(os.path.join(BASE_DIR, 'main/static', 'template.png'))
            draw = ImageDraw.Draw(img)

            text_color = (0, 0, 0)
            font_size = 32
            font = ImageFont.truetype("./arial.ttf", font_size)

            text = donatore.nome.strip() + " " + donatore.cognome.strip()
            text_position = (161, 225)
            draw.text(text_position, text, fill=text_color, font=font)

            text = str(donatore.datadinascita.strftime("%d/%m/%Y"))
            text_position = (311, 275)
            draw.text(text_position, text, fill=text_color, font=font)

            text = donatore.email
            text_position = (152, 325)
            draw.text(text_position, text, fill=text_color, font=font)

            text = donatore.grupposang
            text_position = (374, 375)
            draw.text(text_position, text, fill=text_color, font=font)

            text = str(donatore.tessera)
            text_position = (176, 425)
            draw.text(text_position, text, fill=text_color, font=font)

            fototessera = Image.open(donatore.fototessera).resize((264, 340))
            img.paste(fototessera, (702, 253))

            url = "https://" + request.META['HTTP_HOST'] + "/qr/" + donatore.qrverify
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=5,
                border=0,
            )
            qr.add_data(url)
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color="black", back_color="white")
            img.paste(qr_img, (500, 440))

            image_buffer = BytesIO()
            img.save(image_buffer, format="png")

            nt = "Tessera " + donatore.nome.strip() + " " + donatore.cognome.strip() + ".png"

            response = HttpResponse(image_buffer.getvalue(), content_type="image/png", headers={"Content-Disposition": f'attachment; filename={nt}'})

            return response
    else:
        return redirect("/")
