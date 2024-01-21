from catalog.models import Product
from django.views.generic import ListView, TemplateView


class ProductsListView(ListView):
    model = Product
    template_name = 'catalog/products.html'


class HomeView(TemplateView):
    template_name = 'catalog/home.html'


class ContactView(TemplateView):
    template_name = 'catalog/contacts.html'
