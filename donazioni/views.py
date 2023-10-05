from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from donatori.models import donatori as mDonatori
from .models import donazioni as mDonazioni


@login_required
def salvaDn(request):
    donazioneMod = request.POST.get('donazioneMod')

    lDonazioni = mDonazioni.objects.get(id=donazioneMod)
    lDonazioni.donatore = mDonatori.objects.get(pk=request.POST.get('tessera'))
    lDonazioni.data = request.POST.get('data')
    lDonazioni.tipo = request.POST.get('tipodonazione')
    lDonazioni.quantitativo = request.POST.get('quantitativo')

    lDonazioni.save()
    return redirect("donazioni")


@login_required
def donazioni(request):
    if request.method == 'POST' and 'visualDonazioni' in request.POST:
        template = loader.get_template('visualizzaDonazioni.html')

        if not mDonatori.objects.filter(pk=request.POST.get('visualDonazioni')).exists():
            template = loader.get_template('donazioni.html')
            lDonazioni = mDonazioni.objects.all().order_by('-id')

            paginator = Paginator(lDonazioni, 50)
            page_number = request.GET.get("p")

            page_obj = paginator.get_page(page_number)
            context = {"page_obj": page_obj, "error": "Errore: Numero tessera non valido!"}
            return HttpResponse(template.render(context, request))

        else:
            numeroTessera = request.POST.get('visualDonazioni')

            lDonazioni = mDonazioni.objects.all().filter(donatore_id=numeroTessera).order_by('-id')

            paginator = Paginator(lDonazioni, 50)
            page_number = request.GET.get("p")

            page_obj = paginator.get_page(page_number)
            context = {"page_obj": page_obj, "tessera": numeroTessera}
            return HttpResponse(template.render(context, request))
    elif request.method == 'POST' and 'datadonazione' in request.POST:
        if not mDonatori.objects.filter(pk=request.POST.get('tessera')).exists():
            template = loader.get_template('donazioni.html')
            lDonazioni = mDonazioni.objects.all().order_by('-id')

            paginator = Paginator(lDonazioni, 50)
            page_number = request.GET.get("p")

            page_obj = paginator.get_page(page_number)
            context = {"page_obj": page_obj, "error": "Errore: Numero tessera non valido!"}
            return HttpResponse(template.render(context, request))
        else:
            lDonazioni = mDonazioni.objects.create(donatore_id=request.POST.get('tessera'))

            lDonazioni.data = request.POST.get('datadonazione')
            lDonazioni.tipo = request.POST.get('tipodonazione')
            lDonazioni.quantitativo = request.POST.get('quantitativo')

            lDonazioni.save()

            return redirect("donazioni")
    elif request.method == 'POST' and 'donazioneMod' in request.POST:
        donazioneMod = request.POST.get('donazioneMod')

        if not mDonazioni.objects.filter(id=donazioneMod).exists():
            template = loader.get_template('donazioni.html')
            lDonazioni = mDonazioni.objects.all().order_by('-id')

            paginator = Paginator(lDonazioni, 50)
            page_number = request.GET.get("p")

            page_obj = paginator.get_page(page_number)
            context = {"page_obj": page_obj, "error": "Errore: ID Donazione non valido!"}
            return HttpResponse(template.render(context, request))
        else:
            lDonazioni = mDonazioni.objects.get(id=donazioneMod)
            template = loader.get_template('modificaDonazione.html')
            context = {'donazione': lDonazioni}
            return HttpResponse(template.render(context, request))
    elif request.method == 'POST' and 'donazioneCanc' in request.POST:
        idDonazione = request.POST.get('donazioneCanc')
        lDonazioni = mDonazioni.objects.filter(id=idDonazione).delete()
        return redirect("donazioni")

    else:
        template = loader.get_template('donazioni.html')
        lDonazioni = mDonazioni.objects.all().order_by('-id')

        paginator = Paginator(lDonazioni, 50)
        page_number = request.GET.get("p")

        page_obj = paginator.get_page(page_number)
        context = {"page_obj": page_obj}
        return HttpResponse(template.render(context, request))
