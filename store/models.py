from django.db import models
from cloudinary.models import CloudinaryField


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Phone(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='phones')
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    description = models.TextField(blank=True)

    image = CloudinaryField('image', blank=True, null=True, folder='phones/')
    voice_note = models.FileField(upload_to='voice/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Phones"


# 🛒 CART MODEL (NEW)
class Cart(models.Model):
    session_id = models.CharField(max_length=255)
    phone = models.ForeignKey(Phone, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.phone.name} x {self.quantity}"