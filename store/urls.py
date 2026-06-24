from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.phone_detail, name='phone_detail'),
    
    # Cart
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    
    # Wishlist
    path('wishlist/', views.wishlist, name='wishlist'),
    path('add-to-wishlist/<int:pk>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove-from-wishlist/<int:pk>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    
    # Checkout
    path('checkout/', views.checkout, name='checkout'),
    path('order-success/', views.order_success, name='order_success'),
    
    # Voice
    path('generate-voice/<int:pk>/', views.generate_voice, name='generate_voice'),
    
    # Contact
    path('contact/', views.contact, name='contact'),
    
    # Newsletter
    path('subscribe/', views.subscribe_newsletter, name='subscribe_newsletter'),
    
    # Automated response
    path('auto-response/', views.automated_response, name='auto_response'),
]