from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.conf import settings
from .models import Phone, Category, Cart
import os


# =========================
# HOME
# =========================
def index(request):
    phones = Phone.objects.all()
    categories = Category.objects.prefetch_related('phones')

    return render(request, 'store/index.html', {
        'phones': phones,
        'categories': categories
    })


# =========================
# DETAIL PAGE
# =========================
def phone_detail(request, pk):
    phone = get_object_or_404(Phone, pk=pk)

    return render(request, 'store/phone_detail.html', {
        'phone': phone,
        'store_name': "Yvan Phone Store",
        'map_query': "Nyarugenge Makuza Parking Kigali",
        'google_maps_url': "https://www.google.com/maps?q=Nyarugenge+Makuza+Parking+Kigali"
    })


# =========================
# VOICE GENERATION
# =========================
def generate_voice(request, pk):
    phone = get_object_or_404(Phone, pk=pk)

    if not phone.description:
        return HttpResponse("No description", status=400)

    from gtts import gTTS

    filename = f"phone_{phone.pk}.mp3"
    media_path = os.path.join(settings.MEDIA_ROOT, "voice")
    os.makedirs(media_path, exist_ok=True)

    file_path = os.path.join(media_path, filename)

    if not os.path.exists(file_path):
        tts = gTTS(phone.description, lang="en")
        tts.save(file_path)

        phone.voice_note.name = f"voice/{filename}"
        phone.save()

    return redirect(f"{settings.MEDIA_URL}voice/{filename}")


# =========================
# ADD TO CART
# =========================
def add_to_cart(request, pk):
    phone = get_object_or_404(Phone, pk=pk)

    if not request.session.session_key:
        request.session.create()

    session_id = request.session.session_key

    item, created = Cart.objects.get_or_create(
        session_id=session_id,
        phone=phone
    )

    if not created:
        item.quantity += 1
        item.save()

    return redirect('store:phone_detail', pk=pk)


# =========================
# CART PAGE
# =========================
def cart(request):
    session_id = request.session.session_key
    items = Cart.objects.filter(session_id=session_id)

    total = sum(item.phone.price or 0 * item.quantity for item in items)

    return render(request, 'store/cart.html', {
        'items': items,
        'total': total
    })