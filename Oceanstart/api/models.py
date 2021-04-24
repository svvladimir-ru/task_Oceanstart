from django.db import models


class Category(models.Model):
    """Модель категорий"""
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    """Модель товаров"""
    class PublishedChoices(models.TextChoices):
        YES = 'Опубликован'
        NO = 'Неопубликован'
    name = models.CharField(max_length=50, verbose_name='Название продукта')
    price = models.DecimalField(verbose_name='Цена', max_digits=10, decimal_places=2)
    category = models.ManyToManyField(Category, related_name='category')
    published = models.CharField(max_length=30, choices=PublishedChoices.choices, default=PublishedChoices.NO)
    deleted = models.BooleanField('Товар удален', default=False)