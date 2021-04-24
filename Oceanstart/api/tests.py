from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Product, Category
from .serializers import CategorySerializer, ProductSerializer


class CategoryTest(APITestCase):
    """Тесты категорий"""
    def setUp(self):
        self.category1 = 'Ботинки'
        self.category2 = Category.objects.create(name='Шапки')
        self.category3 = Category.objects.create(name='Носки')
        self.category4 = Category.objects.create(name='Куртки')

        self.product = Product.objects.create(name='Adidas', price=1000,)
        self.product.category.add(self.category2, self.category3)

        self.serializer = CategorySerializer(data={'id': 4, 'name': self.category1}, many=True)

        self.url_create = reverse('create_category')

    def test_create_category(self):
        """Создаем категорию"""
        response = self.client.post(self.url_create, self.serializer.initial_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_category(self):
        """Удаляем категорию"""
        url_delete = reverse('delete_category', args=[self.category4.id])
        response = self.client.delete(url_delete, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_category_error(self):
        """Вызываем 403 при удалении категории с товарами"""
        url_delete = reverse('delete_category', args=[self.category3.id])
        response = self.client.delete(url_delete, format='json')
        message = "Невозможно удалить, в данной категории имеются товары"
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, message)


class ProductTest(APITestCase):
    """Тесты товаров"""
    def setUp(self):
        self.category1 = Category.objects.create(name='Шапки')
        self.category2 = Category.objects.create(name='Носки')

        self.data_error = {'name': 'nike',
                           'price': 2000,
                           'category': [self.category1.name]
                           }
        self.data = {'name': 'adidas',
                     'price': 1000,
                     'category': [
                         self.category1.name,
                         self.category2.name
                     ]}
        self.url_create = reverse('product_list')

    def test_product_create_error(self):
        """Вызываем 400 при попытке создать товар с категорией меньше 2 товаров"""
        serializer = ProductSerializer(data=self.data_error, many=True)
        response = self.client.post(self.url_create, serializer.initial_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_product_create(self):
        """Создаем товар"""
        serializer = ProductSerializer(data=self.data, many=True)
        response = self.client.post(self.url_create, serializer.initial_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
