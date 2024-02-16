from django.contrib import admin
from catalog.models import Category, Product, Version


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'is_published', 'id')
    list_filter = ('category', 'is_published',)
    search_fields = ('name', 'description',)
    list_editable = ('is_published',)  # Поле для редактирования статуса публикации

@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ('product', 'version_number', 'version_name', 'is_current_version')
    list_filter = ('product', 'is_current_version')
    search_fields = ('product__name', 'version_name')
    ordering = ('product', '-version_number')
