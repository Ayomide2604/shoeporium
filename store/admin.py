from django.contrib import admin
from .models import Order, OrderItem, Shoe, Brand, ShoeImage, Cart, CartItem
from django.urls import reverse
from django.utils.html import format_html


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'product_count']


@admin.register(Shoe)
class ShoeAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'price',)
    list_editable = ('price', )
    list_per_page = 20
    list_select_related = ('brand', )
    search_fields = ('name', 'brand__name')


@admin.register(ShoeImage)
class ShoeImageAdmin(admin.ModelAdmin):
    pass


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user__username", "cart_items_count",
                    "view_cart_items_link", "created_at")

    def cart_items_count(self, obj):
        return obj.items.count()
    cart_items_count.short_description = "Total Cart Items"

    def view_cart_items_link(self, obj):
        url = reverse("admin:store_cartitem_changelist") + \
            f"?cart__id__exact={obj.id}"
        return format_html('<a href="{}">View Cart Items</a>', url)
    view_cart_items_link.short_description = "Cart Items"


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['product__name', 'quantity']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "order_items_count",
                    "view_order_items_link", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("user__username",)

    def order_items_count(self, obj):
        return obj.items.count()
    order_items_count.short_description = "Total Order Items"

    def view_order_items_link(self, obj):
        url = reverse("admin:store_orderitem_changelist") + \
            f"?order__id__exact={obj.id}"
        return format_html('<a href="{}">View Order Items</a>', url)
    view_order_items_link.short_description = "Order Items"


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['product__name', 'quantity']
