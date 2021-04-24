from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


class APICategory(APIView):
    """Просмотр(в задаче не указано, добавил для удобства), добавление категорий"""
    def get(self, request):
        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIDetailCategory(APIView):
    """Просмотр удаление категории, добавил get что бы можно было выполнять действия через браузер"""
    def get(self, request, id):
        category = get_object_or_404(Category, id=id)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def delete(self, request, id):
        category = get_object_or_404(Category, id=id)
        if len(category.category.all()) == 0:
            category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=403, data="Невозможно удалить, в данной категории имеются продукты")


class ProductList(generics.ListCreateAPIView):
    """Просмотр всех товаров, либо добавить новый товар"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductFilter


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    """Обновить или удалить товар(просмотр одного товара)"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()
