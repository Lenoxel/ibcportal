from django.shortcuts import render
from .models import EBDClass

def ebd_classes(request):
    ebd_classes = EBDClass.objects.all()
    context = {
        'ebd_classes': ebd_classes
    }
    return render(request, 'ebd/ebd.html', context)
