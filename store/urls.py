from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.index, name='index'),
    path('phone/<int:pk>/', views.phone_detail, name='phone_detail'),
    path('phone/<int:pk>/voice/', views.generate_voice, name='generate_voice'),

    path('cart/add/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
]