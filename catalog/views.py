from django.shortcuts import render
from catalog.models import Product


def home(request):
    context = {
        'title': 'Главная'
    }
    return render(request, 'catalog/home.html', context)


def products(request):
    product_list = Product.objects.all()
    context = {
        'object_list': product_list,
        'title': 'Товары'
    }
    return render(request, 'catalog/products.html', context)


def contacts(request):
    context = {
        'title': 'Контакты'
    }
    return render(request, 'catalog/contacts.html', context)