from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # include your app URLs (store app)
    path('', include('store.urls')),
]