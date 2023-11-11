import os
import qrcode
from jupiter.settings import BASE_DIR
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from donatori.models import donatori as mDonatori
from donazioni.models import donazioni as mDonazioni
from PIL import Image, ImageDraw, ImageFont
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
