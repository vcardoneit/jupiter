from django.shortcuts import render, redirect
from django.contrib.auth import logout as dlogout
from django.contrib.auth import authenticate, login as dlogin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from donatori.models import donatori


@login_required
def logout(request):
    dlogout(request)
    return redirect("login")


def login(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == 'POST' and 'username' in request.POST and 'password' in request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')
            next = request.POST.get('next')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                dlogin(request, user)
                if next:
                    return redirect(next)
                else:
                    return redirect("/")
            else:
                messages.warning(request, "Errore, controlla le tue credenziali!")
                return redirect('login')
        else:
            return render(request, "login.html")


def resetOk(request):
    messages.success(request, "La tua password è stata modificata con successo! Adesso puoi eseguire il login")
    return redirect('login')


def requestOk(request):
    messages.success(request, "Ti abbiamo inviato un'e-mail! (Se non l'hai ricevuta controlla la cartella spam)")
    return redirect('login')


def verifyqr(request, verifycode):
    if donatori.objects.filter(qrverify=verifycode).exists():
        donatore = donatori.objects.get(qrverify=verifycode)
        return render(request, "verifycode.html", {'donatore': donatore})
    else:
        return render(request, "verifycode.html", {'errore': "Tessera non valida!"})
