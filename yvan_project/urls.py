from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from store import views

User = get_user_model()

# ============ TEMPORARY: Admin Creation View ============
def create_admin(request):
    """Temporary view to create admin user - REMOVE AFTER FIRST USE"""
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
            <h2>✅ Password reset for "{username}"!</h2>
            <p><strong>Username:</strong> {username}</p>
            <p><strong>Password:</strong> {password}</p>
            <br>
            <a href="/admin/" style="font-size:20px;">🔐 Go to Admin Panel</a>
            <br><br>
            <a href="/" style="font-size:16px;">🏠 Go to Homepage</a>
        ''')
    else:
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        return HttpResponse(f'''
            <h2>✅ Superuser "{username}" created!</h2>
            <p><strong>Username:</strong> {username}</p>
            <p><strong>Password:</strong> {password}</p>
            <br>
            <a href="/admin/" style="font-size:20px;">🔐 Go to Admin Panel</a>
            <br><br>
            <a href="/" style="font-size:16px;">🏠 Go to Homepage</a>
        ''')

# ============ URL Patterns ============
urlpatterns = [
    path('admin/', admin.site.urls),
    path('create-admin/', create_admin),  # ⚠️ REMOVE THIS AFTER FIRST USE
    path('', views.home, name='home'),  # Your home page view
    # Add other URL patterns here
]

# ============ Serve Media Files in Development ============
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)