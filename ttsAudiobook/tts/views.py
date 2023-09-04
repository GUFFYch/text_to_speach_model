import re
import os
from .models import *
from django.shortcuts import render
from datetime import datetime, date
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt

def Mainpage(request):
    content = {}
    return render(request, 'main.html', content)

def text_to_speech(request):

    # Get the text and name from the request
    text = request.POST['text']
    name = request.POST['name']

    # Generate the audio file
    audio = gTTS(text=text, lang="en", slow=False)
    audio.save(f"{name}.mp3")

    # Redirect the user to the audio playback page
    return HttpResponseRedirect(f"/audio/{name}")

# Create a view to render the audio playback page
def audio_playback(request, name):

    # Get the audio file path
    audio_file_path = f"{name}.mp3"

    # Render the audio playback page
    return render(request, 'audio_playback.html', {
        'audio_file_path': audio_file_path
    })
