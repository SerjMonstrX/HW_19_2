from django.db import models
from django.utils.text import slugify


NULLABLE = {'blank': True, 'null': True}


class BlogPost(models.Model):
    title = models.CharField(max_length=255, verbose_name='заголовок')
    slug = models.CharField(unique=True, max_length=100, verbose_name='адрес', **NULLABLE)
    post_content = models.TextField(verbose_name='содержимое', **NULLABLE)
    preview = models.ImageField(upload_to='blog_previews/', verbose_name='изображение', **NULLABLE)
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    is_published = models.BooleanField(default=False, verbose_name='признак публикации')
    view_count = models.BigIntegerField(default=0,verbose_name='просмотры')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
