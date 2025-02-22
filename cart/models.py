from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import F, Sum

from products.models import Product

class Cart(models.Model):
    user = models.OneToOneField(get_user_model(),
                                on_delete=models.CASCADE,
                                related_name="cart")
    total_price = models.DecimalField(max_digits=10,
                                      decimal_places=2,
                                      default=0.00)

    def __str__(self):
        return f"Cart for {self.user.username}"

    def update_total_price(self):
        """Update shopping basket total price"""
        total = self.items.aggregate(
            total_price=Sum(F('quantity') * F('product__price')))[
                    'total_price'] or 0.00
        self.total_price = total
        self.save()

class CartItem(models.Model):
    cart = models.ForeignKey(Cart,
                             related_name="items",
                             on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='cart_items',
                                on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'product')  # Обеспечиваем уникальность товара в корзине

    def __str__(self):
        return f"{self.product.name} in {self.cart.user.username}'s cart"

    def save(self, *args, **kwargs):
        # При сохранении обновляем сумму корзины
        super().save(*args, **kwargs)
        self.cart.update_total_price()

    def delete(self, *args, **kwargs):
        """When deleting an item, we recalculate
        the total amount of the basket"""
        super().delete(*args, **kwargs)
        self.cart.update_total_price()

    def increase_quantity(self):
        """Increase the number of items in the basket"""
        self.quantity += 1
        self.save()

    def decrease_quantity(self):
        """Reducing the number of items in the basket"""
        if self.quantity > 1:
            self.quantity -= 1
            self.save()
        else:
            self.delete()
