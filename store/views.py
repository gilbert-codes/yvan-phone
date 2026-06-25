from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.conf import settings
from .models import Phone
import os
from gtts import gTTS
import cloudinary.uploader
import tempfile


def index(request):
    phones = Phone.objects.all()
    return render(request, 'store/index.html', {'phones': phones})


def phone_detail(request, pk):
    phone = get_object_or_404(Phone, pk=pk)
    return render(request, 'store/phone_detail.html', {'phone': phone})


def generate_voice(request, pk):
    phone = get_object_or_404(Phone, pk=pk)

    if not phone.description:
        return HttpResponse("No description available")

    # Check if voice already exists
    if phone.voice_note:
        return redirect(phone.voice_note.url)

    # Generate audio
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp:
        tts = gTTS(text=phone.description, lang='en')
        tts.save(tmp.name)
        tmp_path = tmp.name

    try:
        # Upload to Cloudinary
        result = cloudinary.uploader.upload(
            tmp_path,
            resource_type="video",
            folder="voice_notes/"
        )
        
        # Save URL to model
        phone.voice_note = result['secure_url']
        phone.save()
        
        os.unlink(tmp_path)
        return redirect(phone.voice_note)
        
    except Exception as e:
        os.unlink(tmp_path)
        return HttpResponse(f"Error: {str(e)}")