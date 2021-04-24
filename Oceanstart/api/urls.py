from django.urls import path
from .views import APICategory, ProductList, ProductDetail, APIDetailCategory


urlpatterns = [
    path('category/', APICategory.as_view(), name='create_category'),  # добавление категории
    path('category/<int:id>', APIDetailCategory.as_view(), name='delete_category'),  # удаление категории
    path('product/', ProductList.as_view(), name='product_list'),  # просмотр, добавление продуков
    path('product/<int:pk>', ProductDetail.as_view(), name='product_detail'),  # удалить, изменить продукт
]
