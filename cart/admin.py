from django.contrib import admin
from .models import Cart, CartItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price')
    inlines = [CartItemInline]

    def item_count(self, obj):
        """Возвращает количество позиций в корзине."""
        return obj.items.count()

    list_display += ('item_count',)
