from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),

    # your app routes
    path('', include('store.urls')),

    # optional: redirect favicon / homepage safety
    path('', RedirectView.as_view(pattern_name='store:index', permanent=False)),
]