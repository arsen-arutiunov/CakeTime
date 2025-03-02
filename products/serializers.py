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
        extra_kwargs = {
            'name': {'help_text': 'Name of the product'},
            'price': {'help_text': 'Price of the product in USD'},
            'image': {'help_text': 'URL of the product image'},
            'description': {'help_text': 'Description of the product'},
        }

    def validate_category(self, value):
        category_id = value.get('id', None)
        if category_id is None or not Category.objects.filter(
                id=category_id).exists():
            raise serializers.ValidationError("Category does not exist")
        return value
