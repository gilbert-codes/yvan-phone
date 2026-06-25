from django.contrib import admin
from .models import Category, Phone, Cart


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'price', 'created_at']
    list_filter = ['category']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['phone', 'quantity', 'session_id']