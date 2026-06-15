from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Phone, Category
from django.conf import settings
import os

def index(request):
    categories = Category.objects.prefetch_related('phones').all()
    phones = Phone.objects.all().order_by('-created_at')
    return render(request, 'store/index.html', {'phones': phones, 'categories': categories})


def phone_detail(request, pk):
    phone = get_object_or_404(Phone, pk=pk)
    api_key = getattr(settings, 'GOOGLE_MAPS_API_KEY', None)
    if api_key:
        api_key = api_key.strip()
        if not api_key or api_key == 'YOUR_API_KEY_HERE':
            api_key = None

    context = {
        'phone': phone,
        'store_lat': getattr(settings, 'STORE_LAT', None),
        'store_lon': getattr(settings, 'STORE_LON', None),
        'store_name': getattr(settings, 'STORE_NAME', 'Yvan Phone Store'),
        'api_key': api_key,
        'map_query': getattr(settings, 'STORE_MAP_QUERY', 'Nyarugenge near Makuza Parking, Kigali'),
    }
    return render(request, 'store/phone_detail.html', context)


def generate_voice(request, pk):
    # Generate a simple TTS mp3 for the phone description using gTTS.
    phone = get_object_or_404(Phone, pk=pk)
    try:
        from gtts import gTTS
    except Exception:
        return HttpResponse('gTTS not installed on server', status=500)

    if not phone.description:
        return HttpResponse('No description to generate voice from', status=400)

    filename = f'phone_{phone.pk}.mp3'
    out_dir = os.path.join(settings.MEDIA_ROOT, 'voice')
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, filename)

    if not os.path.exists(out_path):
        tts = gTTS(text=phone.description, lang='en')
        tts.save(out_path)
        # save path to model
        phone.voice_note.name = f'voice/{filename}'
        phone.save()

    return redirect(phone.voice_note.url if phone.voice_note else f"{settings.MEDIA_URL}voice/{filename}")
