from django.db import models
from django.contrib.auth import get_user_model

from cart.models import Cart
from products.models import Product


class Order(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Наличные'),
        ('online', 'Онлайн оплата'),
    ]

    PENDING = 'pending'
    COMPLETED = 'completed'
    CANCELED = 'canceled'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (COMPLETED, 'Completed'),
        (CANCELED, 'Canceled'),
    ]

    user = models.ForeignKey(get_user_model(),
                             on_delete=models.CASCADE,
                             related_name='orders')
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE,
                                related_name='order')
    total_price = models.DecimalField(max_digits=10,
                                      decimal_places=2,
                                      default=0.00)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20,
                              choices=STATUS_CHOICES,
                              default=PENDING)

    def __str__(self):
        return f"Order #{self.id} for {self.user.email}"

    def calculate_total(self):
        """Пересчитываем итоговую стоимость заказа."""
        self.total_price = sum([
            item.product.price * item.quantity for item in self.cart.items.all()
        ])
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey('Order',
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} - {self.quantity} pcs"
