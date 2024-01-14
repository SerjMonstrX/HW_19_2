from django.core.management import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):

    def handle(self, *args, **options):
        # Очистка данных
        Category.objects.all().delete()
        Product.objects.all().delete()

        # Список категорий
        category_list = [
            {"name": "Мужская одежда", "description": "Одежда для взрослых мужчин"},
            {"name": "Женская одежда", "description": "Одежда для взрослых женщин"},
            {"name": "Детская одежда", "description": "Одежда для детей"}
        ]

        # Список объектов для bulk_create
        category_for_create = []
        product_for_create = []

        # Создание объектов категорий и продуктов
        for category_item in category_list:
            category = Category(**category_item)
            category_for_create.append(category)

            # Добавление продуктов для каждой категории
            if category.name == "Мужская одежда":
                product_for_create.append(Product(name="Черные джинсы", price=2000, category=category))
                product_for_create.append(Product(name="Кожаная куртка", price=5000, category=category))
            elif category.name == "Женская одежда":
                product_for_create.append(Product(name="Платье в цветочек", price=4000, category=category))
                product_for_create.append(Product(name="Туфли на каблуке", price=8000, category=category))
            elif category.name == "Детская одежда":
                product_for_create.append(Product(name="Детский костюм", price=3000, category=category))
                product_for_create.append(Product(name="Мягкий детский плед", price=2000, category=category))

        # bulk_create для категорий и продуктов
        Category.objects.bulk_create(category_for_create)
        Product.objects.bulk_create(product_for_create)