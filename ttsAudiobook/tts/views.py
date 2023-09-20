import re
import os
from .models import *
from django.shortcuts import render
from datetime import datetime, date
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt

def Mainpage(request):
    content = {}
    texts = Text.objects.all()
    # for text in texts:
        # if 
    print(request.headers['Cookie'].replace('csrftoken=', ''))
    return render(request, 'main.html', content)

def Books(request, pos):
    folder_path = 'books'
    files = os.listdir(folder_path)

    files.sort()

    try:
        pos = int(pos)
    except ValueError:
        pos = 0

    pos = max(0, min(pos, len(files) - 1))
    selected_file = files[pos]
    file_path = os.path.join(folder_path, selected_file)
    print(file_path)
    return render(request, f'books/{file_path}.html', content)

def Settings(request):
    content = {}
    text = Text.objects.all()
    return render(request, 'settings.html', content)
