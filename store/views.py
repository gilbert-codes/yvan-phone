from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.conf import settings
from .models import Phone
import os
from gtts import gTTS


def index(request):
    phones = Phone.objects.all()
    return render(request, 'store/index.html', {'phones': phones})


def phone_detail(request, pk):
    phone = get_object_or_404(Phone, pk=pk)

    return render(request, 'store/phone_detail.html', {
        'phone': phone
    })


def generate_voice(request, pk):
    phone = get_object_or_404(Phone, pk=pk)

    if not phone.description:
        return HttpResponse("No description available")

    filename = f"phone_{phone.pk}.mp3"
    voice_dir = os.path.join(settings.MEDIA_ROOT, "voice")
    os.makedirs(voice_dir, exist_ok=True)

    file_path = os.path.join(voice_dir, filename)

    if not os.path.exists(file_path):
        tts = gTTS(text=phone.description, lang='en')
        tts.save(file_path)

        phone.voice_note = f"voice/{filename}"
        phone.save()

    return redirect(phone.voice_note.url)