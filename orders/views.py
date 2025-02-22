from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=OrderSerializer,
                         responses={201: OrderSerializer})
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(responses={200: OrderSerializer(many=True)})
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(responses={200: OrderSerializer})
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(request_body=OrderSerializer,
                         responses={200: OrderSerializer})
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(request_body=OrderSerializer,
                         responses={200: OrderSerializer})
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(responses={204: 'No Content'})
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        cart = self.request.user.cart
        if not cart.items.exists():
            raise ValidationError(
                "Basket is empty. "
                "Add items to basket before placing an order."
            )

        # Сохраняем заказ
        order = serializer.save(user=self.request.user)
        # Получаем товары из корзины
        cart_items = order.cart.items.all()

        # Создаем элементы заказа на основе товаров из корзины
        for cart_item in cart_items:
            OrderItem.objects.create(order=order, product=cart_item.product,
                                     quantity=cart_item.quantity)
        # Обновляем сумму заказа
        order.calculate_total()

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=OrderItemSerializer,
                         responses={201: OrderItemSerializer})
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(responses={200: OrderItemSerializer(many=True)})
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(responses={200: OrderItemSerializer})
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(request_body=OrderItemSerializer,
                         responses={200: OrderItemSerializer})
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(request_body=OrderItemSerializer,
                         responses={200: OrderItemSerializer})
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(responses={204: 'No Content'})
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
