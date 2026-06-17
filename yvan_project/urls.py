from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from django.contrib.auth import get_user_model

User = get_user_model()

# ---------- Home View ----------
def home(request):
    return HttpResponse('''
        <h1>🏪 Yvan Phone Store</h1>
        <p>📞 Call/Text: 0791364244 — Yvan Lambert</p>
        <p>Welcome to the store!</p>
        <br>
        <a href="/admin/" style="font-size:20px;">🔐 Admin Panel</a>
        <br>
        <a href="/create-admin/" style="font-size:16px;">🔑 Create Admin</a>
    ''')

# ---------- Create Admin View ----------
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
        ''')

# ---------- URL Patterns ----------
urlpatterns = [
    path('admin/', admin.site.urls),
    path('create-admin/', create_admin),  # THIS IS THE KEY URL
    path('', home, name='home'),
]