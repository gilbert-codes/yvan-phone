from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from django.contrib.auth import get_user_model

User = get_user_model()

# ---------- Home View ----------
def home(request):
    from store.models import Phone
    phones = Phone.objects.all()
    
    html = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Yvan Phone Store</title>
            <style>
                body { font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }
                .phone-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 20px; }
                .phone-card { border: 1px solid #ddd; padding: 15px; border-radius: 8px; text-align: center; }
                .phone-card img { max-width: 100%; height: 200px; object-fit: cover; border-radius: 4px; }
                .phone-card h3 { margin: 10px 0; }
                .phone-card .price { color: #2e7d32; font-size: 1.2em; font-weight: bold; }
                .header { text-align: center; padding: 20px 0; background: #f5f5f5; border-radius: 8px; margin-bottom: 20px; }
                .footer { text-align: center; margin-top: 40px; padding: 20px; color: #666; border-top: 1px solid #ddd; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🏪 Yvan Phone Store</h1>
                <p>📞 Call/Text: 0791364244 — Yvan Lambert</p>
            </div>
            
            <h2>📱 Our Phones</h2>
            <div class="phone-grid">
    '''
    
    if phones.exists():
        for phone in phones:
            image_url = phone.image.url if phone.image else ''
            html += f'''
                <div class="phone-card">
                    {f'<img src="{image_url}" alt="{phone.name}">' if image_url else '<p>📱 No image</p>'}
                    <h3>{phone.name}</h3>
                    <p class="price">${phone.price}</p>
                    <p>{phone.description[:100] if phone.description else ''}...</p>
                </div>
            '''
    else:
        html += '<p style="grid-column: 1/-1; text-align: center; padding: 40px;">No phones yet. Check back soon!</p>'
    
    html += '''
            </div>
            <div class="footer">
                <p>© Yvan Phone Store</p>
            </div>
        </body>
        </html>
    '''
    
    return HttpResponse(html)

# ---------- Create/Reset Admin View ----------
def create_admin(request):
    username = 'yvan'
    email = 'yvan@example.com'
    password = 'yvan123'
    
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return HttpResponse(f'''
            <h2>✅ Password reset successful!</h2>
            <p><strong>Username:</strong> {username}</p>
            <p><strong>Password:</strong> {password}</p>
            <br>
            <a href="/admin/">🔐 Go to Admin</a>
            <br>
            <a href="/">🏠 Go to Home</a>
        ''')
    else:
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        return HttpResponse(f'''
            <h2>✅ Superuser created!</h2>
            <p><strong>Username:</strong> {username}</p>
            <p><strong>Password:</strong> {password}</p>
            <br>
            <a href="/admin/">🔐 Go to Admin</a>
            <br>
            <a href="/">🏠 Go to Home</a>
        ''')

# ---------- URL Patterns ----------
urlpatterns = [
    path('admin/', admin.site.urls),
    path('create-admin/', create_admin),
    path('', home, name='home'),
]

# ---------- Serve Media Files ----------
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)