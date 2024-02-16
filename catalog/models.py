from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model


NULLABLE = {'blank': True, 'null': True}


class Version(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='versions', verbose_name='продукт')
    version_number = models.PositiveIntegerField(verbose_name='номер версии', validators=[MinValueValidator(1)])
    version_name = models.CharField(max_length=100, verbose_name='название версии')
    is_current_version = models.BooleanField(default=True, verbose_name='признак текущей версии')

    def __str__(self):
        return f'{self.product.name} - Версия {self.version_number}'

    class Meta:
        verbose_name = 'версия'
        verbose_name_plural = 'версии'
        unique_together = ('product', 'version_number')  # Уникальность номера версии для каждого продукта
        ordering = ['product', '-version_number']  # Сортировка по убыванию номеров версий


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='наименование')
    description = models.TextField(verbose_name='описание', **NULLABLE)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ('name',)


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='наименование')
    description = models.TextField(verbose_name='описание', **NULLABLE)
    image = models.ImageField(upload_to='product_image/', verbose_name='изображение', **NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='категория')
    price = models.IntegerField(verbose_name='цена за штуку')
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    last_change_date = models.DateTimeField(auto_now=True, verbose_name='дата последнего изменения')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=None, null=True,
                             verbose_name='пользователь')
    is_published = models.BooleanField(default=False, verbose_name='Опубликован')

    def __str__(self):
        return f'{self.name}'

    def get_active_version(self):
        return self.versions.filter(is_current_version=True).first()

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ('price',)
