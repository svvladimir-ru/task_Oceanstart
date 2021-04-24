import django_filters
from django_filters import rest_framework as filters

from .models import Product


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    """поиск по имени + вывод нескольких категорий"""
    pass


class IntegerFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    """поиск по id + вывод нескольких категорий"""
    pass


class ProductFilter(django_filters.FilterSet):
    """Фильтрация
    Не совсем понятен пункт f, в фильтрации можно самостоятельно указать
    только по не удаленным"""
    price = filters.RangeFilter()
    category_id = IntegerFilterInFilter(field_name="category__id",
                                        lookup_expr='in')
    category = CharFilterInFilter(field_name="category__name",
                                  lookup_expr='in')

    class Meta:
        model = Product
        fields = ['name', 'category_id', 'category', 'price', 'published', 'deleted']
