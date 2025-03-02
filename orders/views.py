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

    @swagger_auto_schema(
        operation_summary="Get all orders",
        operation_description="Get all orders",
        responses={200: OrderSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create order",
        operation_description="Create a new order",
        request_body=OrderSerializer,
        responses={201: OrderSerializer()}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Get order by ID",
        operation_description="Get order by ID",
        responses={200: OrderSerializer()}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update order by ID",
        operation_description="Update order by ID",
        request_body=OrderSerializer,
        responses={200: OrderSerializer()}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partial update order by ID",
        operation_description="Partial update order by ID",
        request_body=OrderSerializer,
        responses={200: OrderSerializer()}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete order by ID",
        operation_description="Delete order by ID",
        responses={204: "No Content"}
    )
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

    @swagger_auto_schema(
        operation_summary="Get all order items",
        operation_description="Get all order items",
        responses={200: OrderItemSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create order item",
        operation_description="Create order item",
        request_body=OrderItemSerializer,
        responses={201: OrderItemSerializer()}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Get order item by ID",
        operation_description="Get order item by ID",
        responses={200: OrderItemSerializer()}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update order item by ID",
        operation_description="Update order item by ID",
        request_body=OrderItemSerializer,
        responses={200: OrderItemSerializer()}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partial update order item by ID",
        operation_description="Partial update order item by ID",
        request_body=OrderItemSerializer,
        responses={200: OrderItemSerializer()}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete order item by ID",
        operation_description="Delete order item by ID",
        responses={204: "No Content"}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
