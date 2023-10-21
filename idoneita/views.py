from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import idoneita as lIdoneita


@login_required
def idoneita(request):
    if request.user.is_staff:
        listapred = lIdoneita.objects.all().order_by('-dataprelievo')
        paginator = Paginator(listapred, 50)
        page_number = request.GET.get("p")
        page_obj = paginator.get_page(page_number)
        return render(request, "idoneita.html", {'page_obj': page_obj})
    else:
        return redirect("/")


@login_required
def aggiungi(request):
    if request.user.is_staff:
        Idoneita = lIdoneita.objects.create()
        Idoneita.nominativo = request.POST.get('nominativo')
        Idoneita.dataprelievo = request.POST.get('dataprelievo')
        Idoneita.telefono = request.POST.get('telefono')
        Idoneita.email = request.POST.get('email')
        Idoneita.idoneo = request.POST.get('idoneo')
        Idoneita.save()

        messages.success(request, "Predonazione aggiunta con successo!")
        return redirect('idoneita')
    else:
        return redirect("/")


@login_required
def modifica(request):
    if request.user.is_staff:
        idpred = request.POST.get('idpred')

        if not lIdoneita.objects.filter(id=idpred).exists():
            messages.warning(request, "Errore: ID Predonazione non valido!")
            return redirect('idoneita')
        else:
            pred = lIdoneita.objects.get(id=idpred)
            return render(request, "modificaPredonazione.html", {'predonazione': pred})
    else:
        return redirect("/")


@login_required
def salva(request):
    if request.user.is_staff:
        predonazioneMod = request.POST.get('predonazioneMod')
        pred = lIdoneita.objects.get(id=predonazioneMod)
        pred.nominativo = request.POST.get('nominativo')
        pred.dataprelievo = request.POST.get('dataprelievo')
        pred.telefono = request.POST.get('telefono')
        pred.email = request.POST.get('email')
        pred.idoneo = request.POST.get('idoneo')
        pred.save()
        messages.success(request, "Predonazione salvata con successo!")
        return redirect('idoneita')
    return ("/")