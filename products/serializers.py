from rest_framework import serializers
from .models import Product, Category

# Сериализатор для категории
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

# Сериализатор для продукта
class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()  # Включаем категорию в сериализатор продукта

    class Meta:
        model = Product
        fields = '__all__'
