from django.shortcuts import render, redirect
from django.contrib.auth import logout as dlogout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as dlogin
from django.http import HttpResponse
from django.template import loader


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
                template = loader.get_template('login.html')
                context = {'error': "Errore, controlla le tue credenziali!"}
                return HttpResponse(template.render(context, request))
        else:
            return render(request, "login.html")

def resetOk(request):
    template = loader.get_template('login.html')
    context = {"changedpw": "La tua password è stata modificata con successo! Adesso puoi eseguire il login"}
    return HttpResponse(template.render(context, request))