from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.conf import settings
from .models import Phone, Category
import os


# =========================
# HOME PAGE
# =========================
def index(request):
    categories = Category.objects.prefetch_related('phones').all()
    phones = Phone.objects.all().order_by('-created_at')

    return render(request, 'store/index.html', {
        'phones': phones,
        'categories': categories
    })


# =========================
# PHONE DETAIL PAGE
# =========================
def phone_detail(request, pk):
    phone = get_object_or_404(Phone, pk=pk)

    # Safe Google Maps config
    api_key = getattr(settings, 'GOOGLE_MAPS_API_KEY', None)
    if api_key:
        api_key = api_key.strip()
        if api_key == "" or api_key == "YOUR_API_KEY_HERE":
            api_key = None

    context = {
        'phone': phone,
        'store_lat': getattr(settings, 'STORE_LAT', -1.9441),  # Kigali default
        'store_lon': getattr(settings, 'STORE_LON', 30.0619),
        'store_name': getattr(settings, 'STORE_NAME', 'Yvan Phone Store'),
        'api_key': api_key,
        'map_query': getattr(
            settings,
            'STORE_MAP_QUERY',
            'Nyarugenge near Makuza Parking, Kigali'
        ),
    }

    return render(request, 'store/phone_detail.html', context)


# =========================
# VOICE GENERATION (TTS)
# =========================
def generate_voice(request, pk):
    phone = get_object_or_404(Phone, pk=pk)

    if not phone.description:
        return HttpResponse('No description found for voice generation', status=400)

    try:
        from gtts import gTTS
    except Exception:
        return HttpResponse('gTTS is not installed on server', status=500)

    filename = f'phone_{phone.pk}.mp3'
    out_dir = os.path.join(settings.MEDIA_ROOT, 'voice')
    os.makedirs(out_dir, exist_ok=True)

    out_path = os.path.join(out_dir, filename)

    # Generate only if not exists
    if not os.path.exists(out_path):
        tts = gTTS(text=phone.description, lang='en')
        tts.save(out_path)

        # save file path to model (IMPORTANT FIX)
        if hasattr(phone, 'voice_note'):
            phone.voice_note.name = f'voice/{filename}'
            phone.save()

    # Return file safely
    if hasattr(phone, 'voice_note') and phone.voice_note:
        return redirect(phone.voice_note.url)

    return redirect(f"{settings.MEDIA_URL}voice/{filename}")