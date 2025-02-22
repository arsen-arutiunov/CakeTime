from rest_framework import serializers
from .models import Cart, CartItem
from products.models import Product


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name',
                                         read_only=True)
    product_price = serializers.DecimalField(source='product.price',
                                             read_only=True,
                                             max_digits=10,
                                             decimal_places=2)

    class Meta:
        model = CartItem
        fields = [
            'id', 'product', 'quantity', 'product_name', 'product_price'
        ]


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(max_digits=10,
                                           decimal_places=2,
                                           read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'total_price', 'items']
