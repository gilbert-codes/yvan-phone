from django.shortcuts import render, get_object_or_404
from .models import Phone


def index(request):
    phones = Phone.objects.all()
    return render(request, 'store/index.html', {'phones': phones})


def phone_detail(request, pk):
    phone = get_object_or_404(Phone, pk=pk)
    return render(request, 'store/phone_detail.html', {'phone': phone})