from django.core.cache import cache
from django.conf import settings
from .models import Category


def get_categories():
    if settings.CACHE_ENABLED:
        categories = cache.get('categories')
        if not categories:
            categories = list(Category.objects.all())
            cache.set('categories', categories)
    else:
        categories = list(Category.objects.all())
    return categories
