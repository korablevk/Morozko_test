from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse

from products.models import Product


class Blogs(models.Model):
    """
    A model representing a blog.
    """
    title = models.CharField("Название", max_length=250)
    description = models.TextField("Описание", blank=True)
    slug = models.SlugField('URL', max_length=250)
    image = models.ImageField(
        "Изображение", upload_to='images/blog/', blank=True, default='blog/blog/default.jpeg')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField('Дата изменения', auto_now=True)
    products = models.ManyToManyField('Product', blank=True, related_name='blogs', verbose_name='Продукты')

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse("blogs:blog-detail", args=[str(self.slug)])