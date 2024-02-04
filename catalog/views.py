from django.urls import reverse_lazy

from catalog.forms import ProductForm
from catalog.models import Product
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DeleteView, DetailView


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/products.html'


class HomeView(TemplateView):
    template_name = 'catalog/home.html'


class ContactView(TemplateView):
    template_name = 'catalog/contacts.html'


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:products')


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:products')


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:products')


class ProductDetailView(DetailView):
    model = Product
