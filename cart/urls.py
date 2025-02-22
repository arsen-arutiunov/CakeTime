from django.urls import path
from .views import CartAPIView, CartItemAPIView

urlpatterns = [
    path('cart/', CartAPIView.as_view(), name='cart'),
    path('cart/item/', CartItemAPIView.as_view(), name='cart-item-add'),  # Добавить товар в корзину
    path('cart/item/<int:cart_item_id>/',
         CartItemAPIView.as_view(),
         name='cart-item-delete'),  # Удалить товар из корзины
]
