from django.db import models
import uuid
from django.contrib.auth import get_user_model
from cloudinary.models import CloudinaryField

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
    featured_image = CloudinaryField(
        'image', null=True, blank=True, default="https://res.cloudinary.com/dfhvvgzf2/image/upload/v1738714394/default_y0spv5.png")

    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ShoeImage(models.Model):
    shoe = models.ForeignKey(
        Shoe, on_delete=models.CASCADE, related_name='images')
    image = CloudinaryField(
        'image', null=True, blank=True, default="https://res.cloudinary.com/dfhvvgzf2/image/upload/v1738714394/default_y0spv5.png")

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


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('successful', 'Successful'),
        ('failed', 'Failed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')

    def total_order(self):
        return sum(item.subtotal() for item in self.items.all())

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Shoe, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    # Store price at the time of purchase
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def subtotal(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.id}"
