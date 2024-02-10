from django.urls import reverse_lazy
from django.db.models import Prefetch
from catalog.forms import ProductForm, VersionForm
from catalog.models import Product, Version
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DeleteView, DetailView
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/products.html'

    def get_queryset(self):
        # Используем Prefetch для получения связанных версий продуктов
        prefetch_versions = Prefetch('versions', queryset=Version.objects.filter(is_current_version=True),
                                     to_attr='active_versions')
        queryset = Product.objects.prefetch_related(prefetch_versions).all()
        return queryset


class HomeView(TemplateView):
    template_name = 'catalog/home.html'


class ContactView(TemplateView):
    template_name = 'catalog/contacts.html'


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:products')

    def form_valid(self, form):
        # Получаем текущего пользователя
        user = self.request.user
        # Присваиваем текущего пользователя полю user нового продукта
        form.instance.user = user
        # Сохраняем экземпляр модели перед вызовом super().form_valid()
        return super().form_valid(form)

    def get_form_kwargs(self):
        # Получаем ключевые аргументы для формы
        kwargs = super().get_form_kwargs()
        # Изменяем аргументы формы, добавляя пользователя в их начальные значения
        kwargs['initial'] = {'user': self.request.user}
        return kwargs


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:products')

    def test_func(self):
        product = self.get_object()
        return self.request.user == product.user

class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:products')

    def test_func(self):
        product = self.get_object()
        return self.request.user == product.user


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        active_version = product.get_active_version()
        context['active_version'] = active_version
        return context


@login_required
@user_passes_test(lambda u: lambda product_id: u == get_object_or_404(Product, pk=product_id).user, login_url='/login/')
def add_version_to_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        form = VersionForm(request.POST)
        if form.is_valid():
            version = form.save(commit=False)
            version.product = product
            version.save()
            return redirect('catalog:product_detail', pk=product_id)
    else:
        form = VersionForm()

    return render(request, 'catalog/add_version_to_product.html', {'form': form, 'product': product})