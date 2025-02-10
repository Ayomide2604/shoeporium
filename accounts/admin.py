from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile
from django.utils.html import format_html
from django.urls import reverse
# Register your models here.


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', "view_orders_link", "view_cart_link"]

    def view_orders_link(self, obj):
        url = reverse("admin:store_order_changelist") + \
            f"?user__id__exact={obj.id}"
        return format_html('<a href="{}">View Orders</a>', url)

    view_orders_link.short_description = "Orders"

    def view_cart_link(self, obj):
        url = reverse("admin:store_cart_changelist") + \
            f"?user__id__exact={obj.id}"
        return format_html('<a href="{}">View Cart</a>', url)

    view_cart_link.short_description = "Cart"


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'country', 'phone']
    search_fields = ['user__username', 'user__email', 'phone']
    list_filter = ['country']
