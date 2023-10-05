import os
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mass_mail
from donatori.models import donatori


@login_required
def avvisi(request):
    if request.method == 'POST' and 'messaggio' in request.POST:

        oggetto = request.POST.get('oggetto')
        messaggio = request.POST.get('messaggio')
        fromEmail = os.getenv("EMAIL_HOST_USER")
        emailDonatori = donatori.objects.values_list("email", flat=True)

        messaggi = [(oggetto, messaggio, fromEmail, [dest]) for dest in emailDonatori]

        send_mass_mail(messaggi)

        return redirect("avvisi")
    else:
        return render(request, "avvisi.html")
