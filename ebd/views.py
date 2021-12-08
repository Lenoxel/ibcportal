from django.shortcuts import render
from .models import Group

def groups(request):
    groups = Group.objects.all()
    context = {
        'groups': groups
    }
    return render(request, 'ebd/ebd.html', context)
