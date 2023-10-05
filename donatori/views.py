import csv
from django.shortcuts import redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import donatori as mDonatori
from django.template import loader


@login_required
def donatori(request):
    if request.method == 'POST' and 'grupposanguigno' in request.POST and 'datadinascita' in request.POST:
        lDonatori = mDonatori.objects.create()

        lDonatori.grupposang = request.POST.get('grupposanguigno')
        lDonatori.fenotipo = request.POST.get('fenotipo')
        lDonatori.kell = request.POST.get('kell')
        lDonatori.nome = request.POST.get('nome')
        lDonatori.cognome = request.POST.get('cognome')
        lDonatori.datadinascita = request.POST.get('datadinascita')
        lDonatori.luogodinascita = request.POST.get('luogodinascita')
        lDonatori.codicefiscale = request.POST.get('codicefiscale')
        lDonatori.indirizzo = request.POST.get('indirizzo')
        lDonatori.comune = request.POST.get('comune')
        lDonatori.tel = request.POST.get('telefono')
        lDonatori.email = request.POST.get('email')

        lDonatori.save()

        return redirect("donatori")

    elif request.method == 'POST' and 'tesseraMod' in request.POST:
        tesseraMod = request.POST.get('tesseraMod')

        if not mDonatori.objects.filter(tessera=tesseraMod).exists():
            template = loader.get_template('donatori.html')
            lDonatori = mDonatori.objects.all().order_by('-tessera')

            paginator = Paginator(lDonatori, 50)
            page_number = request.GET.get("p")

            page_obj = paginator.get_page(page_number)
            context = {"page_obj": page_obj, "error": "Errore: Numero tessera non valido!"}
            return HttpResponse(template.render(context, request))
        else:
            lDonatori = mDonatori.objects.get(tessera=tesseraMod)
            template = loader.get_template('modifica.html')
            context = {'donatore': lDonatori}
            return HttpResponse(template.render(context, request))

    elif request.method == 'POST' and 'tesseraCanc' in request.POST:
        tesseraCanc = request.POST.get('tesseraCanc')
        lDonatori = mDonatori.objects.filter(tessera=tesseraCanc).delete()
        return redirect("donatori")

    else:
        template = loader.get_template('donatori.html')
        lDonatori = mDonatori.objects.all().order_by('-tessera')

        paginator = Paginator(lDonatori, 50)
        page_number = request.GET.get("p")

        page_obj = paginator.get_page(page_number)
        context = {"page_obj": page_obj}
        return HttpResponse(template.render(context, request))


@login_required
def salva(request):
    tesseraMod = request.POST.get('tesseraMod')

    lDonatori = mDonatori.objects.get(tessera=tesseraMod)

    lDonatori.grupposang = request.POST.get('grupposanguigno')
    lDonatori.fenotipo = request.POST.get('fenotipo')
    lDonatori.kell = request.POST.get('kell')
    lDonatori.nome = request.POST.get('nome')
    lDonatori.cognome = request.POST.get('cognome')
    lDonatori.datadinascita = request.POST.get('datadinascita')
    lDonatori.luogodinascita = request.POST.get('luogodinascita')
    lDonatori.codicefiscale = request.POST.get('codicefiscale')
    lDonatori.indirizzo = request.POST.get('indirizzo')
    lDonatori.comune = request.POST.get('comune')
    lDonatori.tel = request.POST.get('telefono')
    lDonatori.email = request.POST.get('email')

    lDonatori.save()
    return redirect("donatori")

@login_required
def esporta(request):
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="donatori.csv"'},
    )

    lDonatori = mDonatori.objects.all()

    writer = csv.writer(response)
    writer.writerow(["tessera", "grupposang", "fenotipo", "kell", "nome", "cognome", "datadinascita", "luogodinascita", "codicefiscale", "indirizzo", "comune", "tel", "email"])
    for x in lDonatori:
        writer.writerow([x.tessera, x.grupposang, x.fenotipo, x.kell, x.nome, x.cognome, x.datadinascita, x.luogodinascita, x.codicefiscale, x.indirizzo, x.comune, x.tel, x.email])

    return response