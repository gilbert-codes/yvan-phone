from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.conf import settings
from .models import Phone, Cart
import os


def index(request):
    phones = Phone.objects.all()
    return render(request, 'store/index.html', {'phones': phones})


def phone_detail(request, pk):
    phone = get_object_or_404(Phone, pk=pk)

    return render(request, 'store/phone_detail.html', {
        'phone': phone,
        'google_maps_url': "https://www.google.com/maps?q=Makuza+Peace+Plaza+Kigali"
    })


def generate_voice(request, pk):
    phone = get_object_or_404(Phone, pk=pk)

    if not phone.description:
        return HttpResponse("No description")

    from gtts import gTTS

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


def add_to_cart(request, pk):
    phone = get_object_or_404(Phone, pk=pk)

    if not request.session.session_key:
        request.session.create()

    session_id = request.session.session_key

    item, created = Cart.objects.get_or_create(
        session_id=session_id,
        phone=phone,
        defaults={'quantity': 1}
    )

    if not created:
        item.quantity += 1
        item.save()

    return redirect('store:phone_detail', pk=pk)


def cart(request):
    session_id = request.session.session_key
    items = Cart.objects.filter(session_id=session_id)

    total = sum((item.phone.price or 0) * item.quantity for item in items)

    return render(request, 'store/cart.html', {
        'items': items,
        'total': total
    })