from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from donatori.models import donatori as mDonatori
from donazioni.models import donazioni as mDonazioni


@login_required
def index(request):
    if request.user.is_staff:
        return render(request, "index.html")
    else:
        donatore = mDonatori.objects.get(email=request.user.username)
        totDonazioni = mDonazioni.objects.filter(donatore_id=donatore.tessera).count()
        template = loader.get_template('index.html')
        print(totDonazioni)
        context = {"donatore": donatore, "totDonazioni": totDonazioni}
        return HttpResponse(template.render(context, request))
