from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from products.models import Product
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer


class CartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get the current user's basket",
        responses={
            200: CartSerializer(),
            400: openapi.Response("Your cart is empty")
        }
    )
    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        if not cart.items.exists():  # Если корзина пуста
            return Response({'detail': 'Your cart is empty'},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a shopping basket "
                              "for the user (if it does not exist)",
        responses={201: CartSerializer()}
    )
    def post(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CartItemAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Add item to basket",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'product': openapi.Schema(type=openapi.TYPE_INTEGER,
                                          description='Product ID'),
                'quantity': openapi.Schema(type=openapi.TYPE_INTEGER,
                                           description='Quantity',
                                           default=1),
            },
            required=['product']
        ),
        responses={
            201: CartItemSerializer(),
            404: openapi.Response("Product not found")
        }
    )
    def post(self, request):
        product_id = request.data.get('product')
        quantity = request.data.get('quantity', 1)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'detail': 'Product not found'},
                            status=status.HTTP_404_NOT_FOUND)

        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart,
                                                            product=product)

        # Обновляем количество товара
        cart_item.quantity += quantity
        cart_item.save()

        # Обновляем общую цену корзины
        cart.update_total_price()

        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description="Remove an item from the basket",
        manual_parameters=[
            openapi.Parameter('cart_item_id', openapi.IN_PATH,
                              description="basket item ID",
                              type=openapi.TYPE_INTEGER)
        ],
        responses={
            204: openapi.Response("Item removed from cart"),
            404: openapi.Response("Cart item not found")
        }
    )
    def delete(self, request, cart_item_id):
        try:
            cart_item = CartItem.objects.get(id=cart_item_id,
                                             cart__user=request.user)
        except CartItem.DoesNotExist:
            return Response({'detail': 'Cart item not found'},
                            status=status.HTTP_404_NOT_FOUND)

        cart_item.delete()

        cart = Cart.objects.get(user=request.user)
        cart.update_total_price()

        return Response({'detail': 'Item removed from cart'},
                        status=status.HTTP_204_NO_CONTENT)
