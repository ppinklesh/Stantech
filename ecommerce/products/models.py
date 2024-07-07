from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import AbstractUser

class Product(models.Model):
    product_id = models.CharField(max_length=100, primary_key=True)
    product_name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    price = models.FloatField()
    quantity_sold = models.IntegerField()
    rating = models.FloatField()
    review_count = models.IntegerField()

class User(AbstractUser):
    pass
