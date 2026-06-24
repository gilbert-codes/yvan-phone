from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.index, name='index'),

    # phone detail page
    path('phone/<int:pk>/', views.phone_detail, name='phone_detail'),

    # optional voice endpoint (if you want API-style voice later)
    path('phone/<int:pk>/generate-voice/', views.generate_voice, name='generate_voice'),
]