from django.contrib import admin
from .models import Category, Phone


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
    ordering = ['name']          # ✅ faster + alphabetical
    list_per_page = 20          # ✅ pagination for speed


@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'price', 'created_at']
    
    list_filter = ['category', 'created_at']
    search_fields = ['name', 'description']
    
    readonly_fields = ['created_at']
    
    fields = [
        'name',
        'category',
        'price',
        'description',
        'image',
        'voice_note',
        'created_at'
    ]

    ordering = ['-created_at']   # ✅ newest first
    list_per_page = 25           # ✅ faster admin loading