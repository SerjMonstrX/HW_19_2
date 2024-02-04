from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import ContactView, ProductListView, HomeView, ProductCreateView, ProductUpdateView, ProductDeleteView, ProductDetailView, add_version_to_product


app_name = CatalogConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contacts/', ContactView.as_view(), name='contacts'),
    path('products/', ProductListView.as_view(), name='products'),
    path('products/create/', ProductCreateView.as_view(), name='create_product'),
    path('products/detail/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/update/<int:pk>/', ProductUpdateView.as_view(), name='update_product'),
    path('products/delete/<int:pk>/', ProductDeleteView.as_view(), name='delete_product'),
    path('products/add_version/<int:product_id>/', add_version_to_product, name='add_version_to_product'),
]
