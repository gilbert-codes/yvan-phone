from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.index, name='index'),
    path('phone/<int:pk>/', views.phone_detail, name='phone_detail'),
]