from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import contacts, ProductsListView, HomeView


app_name = CatalogConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contacts/', contacts, name='contacts'),
    path('products/', ProductsListView.as_view(), name='products'),
]
