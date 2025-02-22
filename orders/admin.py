from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'user', 'status', 'total_price', 'payment_method', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('user__email', 'user__username')
    readonly_fields = ('total_price', 'created_at')

    def cart_items(self, obj):
        """Отображаем товары из корзины"""
        return ", ".join([f"{item.product.name} ({item.quantity})" for item in
                          obj.cart.items.all()])

    cart_items.short_description = "Товары в заказе"

    fieldsets = (
        (None, {"fields": (
        "user", "cart", "total_price", "payment_method", "status",
        "created_at")}),
    )

    list_display += ('cart_items',)  # Добавляем в список отображения
