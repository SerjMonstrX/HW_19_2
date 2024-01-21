from django.shortcuts import render
from catalog.models import Product
from django.views.generic import ListView, TemplateView


class ProductsListView(ListView):
    model = Product
    template_name = 'catalog/products.html'


class HomeView(TemplateView):
    template_name = 'catalog/home.html'


def contacts(request):
    context = {
        'title': 'Контакты'
    }
    return render(request, 'catalog/contacts.html', context)
