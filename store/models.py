from django.db import models
import uuid
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()


class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def product_count(self):
        return self.shoes.count()

    product_count.short_description = "Number of Products"

    def __str__(self):
        return self.name


class Shoe(models.Model):
    name = models.CharField(max_length=255)
    brand = models.ForeignKey(
        Brand, on_delete=models.SET_NULL, related_name='shoes', null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(
        upload_to='shoes', null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ShoeImage(models.Model):
    shoe = models.ForeignKey(
        Shoe, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='shoes')

    def __str__(self):
        return f'image of {self.shoe.name}'


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def total_items(self):
        return self.items.count()

    def total_cart(self):
        return sum(item.subtotal() for item in self.items.all())

    def __str__(self):
        return f"Cart - {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name="items")

    product = models.ForeignKey(Shoe, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.cart.user.username}'s cart"

    class Meta:
        unique_together = ("cart", "product")
