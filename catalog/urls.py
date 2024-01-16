from django.urls import path

from catalog.views import home, contacts, products

urlpatterns = [
    path('', home, name='home'),
    path('contacts/', contacts, name='contacts'),
    path('products/', products, name='products'),
]