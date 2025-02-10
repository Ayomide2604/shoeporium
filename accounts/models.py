from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class CustomUser(AbstractUser):

    pass


class Profile(models.Model):
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='profile')
    address = models.CharField(max_length=200, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    profile_image = CloudinaryField(
        'image', default="https://res.cloudinary.com/dfhvvgzf2/image/upload/v1739183725/profile_xhxjdh.png")

    def __str__(self):
        return f"{self.user.username}'s Profile"
