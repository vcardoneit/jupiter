from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from donazioni.models import donazioni
from donatori.models import donatori

# Create your views here.
@login_required
def statistiche(request):
    
    return render(request,template_name="statistiche.html")