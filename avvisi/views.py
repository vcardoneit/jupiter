import os
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mass_mail
from donatori.models import donatori


@login_required
def avvisi(request):
    if request.user.is_staff:
        if request.method == 'POST' and 'messaggio' in request.POST:

            oggetto = request.POST.get('oggetto')
            messaggio = request.POST.get('messaggio')
            fromEmail = os.getenv("DEFAULT_FROM_EMAIL")

            if request.POST.get('tipoMsg') == "convocazione":
                emailDonatori = donatori.objects.values_list("email", flat=True).filter(privacy_b=True)

            if request.POST.get('tipoMsg') == "pubblicita":
                emailDonatori = donatori.objects.values_list("email", flat=True).filter(privacy_c=True)

            messaggi = [(oggetto, messaggio, fromEmail, [dest]) for dest in emailDonatori]

            send_mass_mail(messaggi)

            messages.success(request, "Email inviate con successo!")
            return redirect("avvisi")
        else:
            return render(request, "avvisi.html")
    else:
        return redirect("/")
