from django.contrib import admin
from .models import Shoe, Brand, ShoeImage, Cart, CartItem


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'product_count']


@admin.register(Shoe)
class ShoeAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'price')
    list_per_page = 20
    search_fields = ('name', 'brand__name')


@admin.register(ShoeImage)
class ShoeImageAdmin(admin.ModelAdmin):
    pass


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    pass


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    pass
