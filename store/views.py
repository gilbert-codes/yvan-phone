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

    # Check if voice already exists in Cloudinary
    if phone.voice_note and phone.voice_note.startswith('http'):
        return redirect(phone.voice_note)

    # Generate audio locally first
    filename = f"phone_{phone.pk}.mp3"
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
        tts = gTTS(text=phone.description, lang='en')
        tts.save(tmp_file.name)
        tmp_file_path = tmp_file.name

    try:
        # Upload to Cloudinary
        upload_result = cloudinary.uploader.upload(
            tmp_file_path,
            resource_type="video",  # video includes audio files
            folder="voice_notes/",
            public_id=f"phone_{phone.pk}"
        )
        
        # Save Cloudinary URL to model
        phone.voice_note = upload_result['secure_url']
        phone.save()
        
        # Clean up temp file
        os.unlink(tmp_file_path)
        
        return redirect(phone.voice_note)
        
    except Exception as e:
        # Clean up temp file
        if os.path.exists(tmp_file_path):
            os.unlink(tmp_file_path)
        return HttpResponse(f"Error generating voice: {str(e)}")