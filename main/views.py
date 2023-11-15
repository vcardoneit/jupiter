import os
import qrcode
from jupiter.settings import BASE_DIR
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from donatori.models import donatori as mDonatori
from donazioni.models import donazioni as mDonazioni
from PIL import Image, ImageDraw, ImageFont
from django.contrib import messages
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.shortcuts import get_object_or_404
from datetime import datetime
from io import BytesIO


@login_required
def index(request):
    if request.user.is_staff:
        return render(request, "index.html")
    else:
        donatore = mDonatori.objects.get(email=request.user.username)
        totDonazioni = mDonazioni.objects.filter(donatore_id=donatore.tessera).count()
        return render(request, "index.html", {"donatore": donatore, "totDonazioni": totDonazioni})


@login_required
def tessera(request):
    if request.user.is_staff:
        return redirect("/")
    else:
        donatore = mDonatori.objects.get(email=request.user.username)

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


@login_required
def autorizzazione(request):
    if request.user.is_staff or mDonatori.objects.get(email=request.user.email).autorizzazione:
        return redirect("/")
    else:
        donatore = mDonatori.objects.get(email=request.user.username)
        return render(request, "autorizzazione.html", {"donatore": donatore})


@login_required
def autorizza(request):
    if request.user.is_staff or mDonatori.objects.get(email=request.user.email).autorizzazione:
        return redirect("/")
    else:
        img = Image.open(os.path.join(BASE_DIR, 'main/static', 'autoreferti.png'))

        draw = ImageDraw.Draw(img)

        text_color = (0, 0, 0)
        font_size = 64
        font = ImageFont.truetype("./arial.ttf", font_size)

        text = request.POST.get('nomecompleto')
        text_position = (676, 993)
        draw.text(text_position, text, fill=text_color, font=font)

        text = request.POST.get('luogodinascita')
        text_position = (1656, 993)
        draw.text(text_position, text, fill=text_color, font=font)

        text = datetime.strptime(request.POST.get('datadinascita'), '%Y-%m-%d').strftime('%d/%m/%Y')
        text_position = (220, 1120)
        draw.text(text_position, text, fill=text_color, font=font)

        text = request.POST.get('luogodiresidenza')
        text_position = (1350, 1120)
        draw.text(text_position, text, fill=text_color, font=font)

        text = request.POST.get('indirizzodiresidenza')
        text_position = (530, 1240)
        draw.text(text_position, text, fill=text_color, font=font)

        text = request.POST.get('numdocumento')
        text_position = (715, 1555)
        draw.text(text_position, text, fill=text_color, font=font)

        text = request.POST.get('rilasciodoc')
        text_position = (1590, 1555)
        draw.text(text_position, text, fill=text_color, font=font)

        text = datetime.strptime(request.POST.get('datrilasciodoc'), '%Y-%m-%d').strftime('%d/%m/%Y')
        text_position = (210, 1680)
        draw.text(text_position, text, fill=text_color, font=font)

        text = datetime.strptime(request.POST.get('scadoc'), '%Y-%m-%d').strftime('%d/%m/%Y')
        text_position = (1055, 1680)
        draw.text(text_position, text, fill=text_color, font=font)

        image_buffer = BytesIO()
        img.save(image_buffer, format="png")
        image_buffer.seek(0)

        lDonatori = mDonatori.objects.get(email=request.user.email)
        lDonatori.autorizzazione = InMemoryUploadedFile(image_buffer, None, "Autorizzazione " + lDonatori.nome + " " + lDonatori.cognome + ".png", 'image/png', image_buffer.tell(), None)
        lDonatori.save()

        return redirect("/")


@login_required
def autdownload(request, dId):
    if request.user.is_staff:
        donatore = get_object_or_404(mDonatori, tessera=dId)
        try:
            response = HttpResponse(donatore.autorizzazione.file, content_type='image/png')
            response['Content-Disposition'] = 'attachment; filename={}'.format("Autorizzazione " + donatore.nome + " " + donatore.cognome + ".png")
            return response
        except Exception:
            messages.warning(request, "File non trovato!")
            return redirect("donatori")
    else:
        return redirect("/")
