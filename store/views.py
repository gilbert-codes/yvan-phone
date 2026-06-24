from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from .models import Phone, Category, Cart, Order, Testimonial, Newsletter, Wishlist
from django.conf import settings
import os
import json
from django.core.mail import send_mail

# ---------- HOME PAGE ----------
def home(request):
    categories = Category.objects.filter(is_active=True)
    featured_phones = Phone.objects.filter(is_available=True)[:8]
    new_phones = Phone.objects.filter(is_available=True).order_by('-created_at')[:6]
    testimonials = Testimonial.objects.filter(is_approved=True).order_by('-created_at')[:4]
    
    context = {
        'categories': categories,
        'featured_phones': featured_phones,
        'new_phones': new_phones,
        'testimonials': testimonials,
        'store_name': getattr(settings, 'STORE_NAME', 'Yvan Phone Store'),
        'store_lat': getattr(settings, 'STORE_LAT', '-1.9441'),
        'store_lon': getattr(settings, 'STORE_LON', '30.0619'),
        'google_maps_api_key': getattr(settings, 'GOOGLE_MAPS_API_KEY', None),
    }
    return render(request, 'store/home.html', context)


# ---------- PRODUCT LIST PAGE ----------
def product_list(request):
    category_slug = request.GET.get('category')
    search_query = request.GET.get('q')
    
    phones = Phone.objects.filter(is_available=True)
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        phones = phones.filter(category=category)
    
    if search_query:
        phones = phones.filter(name__icontains=search_query)
    
    # Sort
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'price_low':
        phones = phones.order_by('discounted_price')
    elif sort_by == 'price_high':
        phones = phones.order_by('-discounted_price')
    elif sort_by == 'popular':
        phones = phones.order_by('-views')
    else:
        phones = phones.order_by('-created_at')
    
    categories = Category.objects.filter(is_active=True)
    
    context = {
        'phones': phones,
        'categories': categories,
        'current_category': category_slug,
        'search_query': search_query,
        'sort_by': sort_by,
    }
    return render(request, 'store/product_list.html', context)


# ---------- PHONE DETAIL ----------
def phone_detail(request, pk):
    phone = get_object_or_404(Phone, pk=pk)
    
    # Increment views
    phone.views += 1
    phone.save()
    
    # Related phones
    related_phones = Phone.objects.filter(
        category=phone.category, 
        is_available=True
    ).exclude(id=phone.id)[:4]
    
    # Testimonials for this phone
    testimonials = Testimonial.objects.filter(phone=phone, is_approved=True)
    
    context = {
        'phone': phone,
        'related_phones': related_phones,
        'testimonials': testimonials,
        'store_lat': getattr(settings, 'STORE_LAT', '-1.9441'),
        'store_lon': getattr(settings, 'STORE_LON', '30.0619'),
        'store_name': getattr(settings, 'STORE_NAME', 'Yvan Phone Store'),
        'api_key': getattr(settings, 'GOOGLE_MAPS_API_KEY', None),
    }
    return render(request, 'store/phone_detail.html', context)


# ---------- ADD TO CART ----------
def add_to_cart(request, pk):
    phone = get_object_or_404(Phone, pk=pk)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
    else:
        quantity = 1
    
    # Get or create session_id
    if not request.session.session_key:
        request.session.create()
    session_id = request.session.session_key
    
    cart_item, created = Cart.objects.get_or_create(
        session_id=session_id,
        phone=phone,
        defaults={'quantity': quantity}
    )
    
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    
    messages.success(request, f"{phone.name} added to cart!")
    
    if request.method == 'POST' and request.POST.get('next'):
        return redirect(request.POST.get('next'))
    return redirect('store:cart')


# ---------- VIEW CART ----------
def cart(request):
    if not request.session.session_key:
        request.session.create()
    
    cart_items = Cart.objects.filter(session_id=request.session.session_key)
    total = sum(item.get_total_price() for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'store/cart.html', context)


# ---------- REMOVE FROM CART ----------
def remove_from_cart(request, pk):
    cart_item = get_object_or_404(Cart, pk=pk, session_id=request.session.session_key)
    cart_item.delete()
    messages.success(request, "Item removed from cart")
    return redirect('store:cart')


# ---------- CHECKOUT ----------
def checkout(request):
    if not request.session.session_key:
        request.session.create()
    
    cart_items = Cart.objects.filter(session_id=request.session.session_key)
    
    if not cart_items:
        messages.error(request, "Your cart is empty")
        return redirect('store:cart')
    
    total = sum(item.get_total_price() for item in cart_items)
    
    if request.method == 'POST':
        # Create order
        order = Order.objects.create(
            session_id=request.session.session_key,
            full_name=request.POST.get('full_name'),
            email=request.POST.get('email'),
            phone_number=request.POST.get('phone_number'),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            country=request.POST.get('country', 'Rwanda'),
            items=[{
                'name': item.phone.name,
                'quantity': item.quantity,
                'price': str(item.phone.price),
                'total': str(item.get_total_price())
            } for item in cart_items],
            subtotal=total,
            shipping_fee=0,
            total=total,
            notes=request.POST.get('notes', ''),
        )
        
        # Clear cart
        cart_items.delete()
        
        # Send email notification
        try:
            send_mail(
                f'New Order #{order.order_number}',
                f"Order received from {order.full_name}\nTotal: ${order.total}",
                'noreply@yvanphone.com',
                ['your-email@example.com'],
                fail_silently=True,
            )
        except:
            pass
        
        messages.success(request, f"Order #{order.order_number} placed successfully!")
        return redirect('store:order_success')
    
    context = {
        'cart_items': cart_items,
        'total': total,
        'store_lat': getattr(settings, 'STORE_LAT', '-1.9441'),
        'store_lon': getattr(settings, 'STORE_LON', '30.0619'),
    }
    return render(request, 'store/checkout.html', context)


# ---------- ORDER SUCCESS ----------
def order_success(request):
    return render(request, 'store/order_success.html')


# ---------- WISHLIST ----------
def add_to_wishlist(request, pk):
    phone = get_object_or_404(Phone, pk=pk)
    
    if not request.session.session_key:
        request.session.create()
    
    wishlist, created = Wishlist.objects.get_or_create(
        session_id=request.session.session_key,
        phone=phone
    )
    
    if created:
        messages.success(request, f"{phone.name} added to wishlist")
    else:
        messages.info(request, f"{phone.name} already in wishlist")
    
    return redirect('store:wishlist')


def wishlist(request):
    if not request.session.session_key:
        request.session.create()
    
    wishlist_items = Wishlist.objects.filter(session_id=request.session.session_key)
    return render(request, 'store/wishlist.html', {'wishlist_items': wishlist_items})


def remove_from_wishlist(request, pk):
    wishlist_item = get_object_or_404(Wishlist, pk=pk, session_id=request.session.session_key)
    wishlist_item.delete()
    messages.success(request, "Item removed from wishlist")
    return redirect('store:wishlist')


# ---------- NEWSLETTER ----------
def subscribe_newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            Newsletter.objects.get_or_create(email=email)
            messages.success(request, "Subscribed to newsletter!")
        else:
            messages.error(request, "Please enter a valid email")
    return redirect(request.META.get('HTTP_REFERER', 'store:home'))


# ---------- CONTACT ----------
def contact(request):
    context = {
        'store_lat': getattr(settings, 'STORE_LAT', '-1.9441'),
        'store_lon': getattr(settings, 'STORE_LON', '30.0619'),
        'store_name': getattr(settings, 'STORE_NAME', 'Yvan Phone Store'),
        'api_key': getattr(settings, 'GOOGLE_MAPS_API_KEY', None),
    }
    return render(request, 'store/contact.html', context)


# ---------- GENERATE VOICE ----------
def generate_voice(request, pk):
    phone = get_object_or_404(Phone, pk=pk)
    
    try:
        from gtts import gTTS
    except Exception:
        return HttpResponse('gTTS not installed', status=500)
    
    if not phone.description:
        return HttpResponse('No description', status=400)
    
    filename = f'phone_{phone.pk}.mp3'
    out_dir = os.path.join(settings.MEDIA_ROOT, 'voice')
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, filename)
    
    if not os.path.exists(out_path):
        tts = gTTS(text=phone.description, lang='en')
        tts.save(out_path)
        phone.voice_note.name = f'voice/{filename}'
        phone.save()
    
    return redirect(phone.voice_note.url if phone.voice_note else f"{settings.MEDIA_URL}voice/{filename}")


# ---------- AUTOMATED RESPONSE ----------
def automated_response(request):
    if request.method == 'POST':
        message = request.POST.get('message', '').lower()
        
        responses = {
            'price': "💰 Our phones range from $100 to $1500. Check our collection!",
            'delivery': "🚚 We deliver within 24-48 hours in Kigali.",
            'warranty': "✅ All phones come with 12 months warranty.",
            'return': "🔄 7-day return policy for defective items.",
            'payment': "💳 We accept Mobile Money, Bank Transfer, and Cash.",
            'contact': "📞 Call us at 0791364244 or visit our store.",
            'default': "📱 Hi! How can I help you? I can assist with prices, delivery, warranty, and more."
        }
        
        response = responses['default']
        for key, value in responses.items():
            if key in message:
                response = value
                break
        
        return JsonResponse({'response': response})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)