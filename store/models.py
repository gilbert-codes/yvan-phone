from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="FontAwesome icon class")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.name.lower().replace(' ', '-')
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']


class Phone(models.Model):
    CONDITION_CHOICES = [
        ('new', 'Brand New'),
        ('refurbished', 'Refurbished'),
        ('used', 'Pre-owned'),
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='phones')
    
    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Original price before discount")
    discount_percent = models.IntegerField(default=0, help_text="Discount percentage")
    
    # Details
    description = models.TextField(blank=True)
    specifications = models.JSONField(default=dict, blank=True, help_text="Technical specifications as JSON")
    
    # Images
    image = CloudinaryField('image', blank=True, null=True, folder='phones/')
    image_2 = CloudinaryField('image', blank=True, null=True, folder='phones/')
    image_3 = CloudinaryField('image', blank=True, null=True, folder='phones/')
    
    # Media
    voice_note = models.FileField(upload_to='voice/', blank=True, null=True)
    video_url = models.URLField(blank=True, help_text="YouTube or video URL for advertisement")
    
    # Inventory
    stock = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='new')
    
    # Features
    features = models.JSONField(default=list, blank=True, help_text="List of key features")
    color_options = models.JSONField(default=list, blank=True, help_text="Available colors")
    
    # SEO
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True, max_length=500)
    seo_keywords = models.CharField(max_length=500, blank=True)
    
    # Tracking
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.name.lower().replace(' ', '-')
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Phones"

    @property
    def discounted_price(self):
        if self.discount_percent > 0:
            return self.price - (self.price * self.discount_percent / 100)
        return self.price


class Cart(models.Model):
    session_id = models.CharField(max_length=255)
    phone = models.ForeignKey(Phone, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.phone.name} x {self.quantity}"

    def get_total_price(self):
        return self.quantity * (self.phone.discounted_price or self.phone.price)


class Order(models.Model):
    ORDER_STATUS = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    order_number = models.CharField(max_length=20, unique=True)
    session_id = models.CharField(max_length=255)
    
    # Customer info
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='Rwanda')
    
    # Order details
    items = models.JSONField(default=list, help_text="List of ordered items")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Status
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')
    payment_method = models.CharField(max_length=50, blank=True)
    payment_status = models.CharField(max_length=20, default='pending')
    
    # Tracking
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.order_number} - {self.full_name}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            import random
            import string
            self.order_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        super().save(*args, **kwargs)


class Testimonial(models.Model):
    customer_name = models.CharField(max_length=100)
    phone = models.ForeignKey(Phone, on_delete=models.SET_NULL, null=True, blank=True)
    rating = models.PositiveIntegerField(default=5, choices=[(1,1),(2,2),(3,3),(4,4),(5,5)])
    comment = models.TextField()
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.customer_name} - {self.rating}★"


class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email


class Wishlist(models.Model):
    session_id = models.CharField(max_length=255)
    phone = models.ForeignKey(Phone, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.phone.name} - Wishlist"