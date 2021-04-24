from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    """Создание и вывод категории"""
    class Meta:
        model = Category
        fields = ['id', 'name', ]


class ProductSerializer(serializers.ModelSerializer):
    """Создание и вывод продукта"""
    category = serializers.SlugRelatedField(slug_field='name',
                                            queryset=Category.objects.all(),
                                            many=True,
                                            )

    def validate_category(self, category):
        if len(category) < 2 or len(category) > 10:
            raise ValidationError(
                'Товар должен иметь от 2 до 10 категорий!')
        return category

    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'price', 'published']
