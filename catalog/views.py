from django.shortcuts import render
from catalog.models import Product


def home(request):
    return render(request, 'catalog/home.html')


def products(request):
    product_list = Product.objects.all()
    context = {
        'object_list': product_list
    }
    return render(request, 'catalog/products.html', context)


def contacts(request):
    return render(request, 'catalog/contacts.html')