import re
import os
from .models import *
from django.shortcuts import render
from datetime import datetime, date
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt

# get user current ip address
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def Mainpage(request):
    content = {}
    content['books'] = Book.objects.all()
    user_ip = get_client_ip(request)
    texts = Text.objects.all()
    user_existence = False
    for text in texts:
        if user_ip in text.user:
            user_existence = True
    if not(user_existence):
        Text.objects.create(user = user_ip)    
    
    return render(request, 'main.html', content)

def Books(request, name):
    content = {}
    content['book'] = Book.objects.get(name = name.replace("%0%", " "))
    
    return render(request, 'audiobooks.html', content)

def Settings(request):
    content = {}
    text = Text.objects.all()
    return render(request, 'settings.html', content)
