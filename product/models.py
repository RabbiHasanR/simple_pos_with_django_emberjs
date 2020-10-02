from django.db import models


class Product(models.Model):
    """A model that contains data for a single product."""
    title = models.CharField(max_length=255, default="")
    price = models.CharField(max_length=255, default="")
    category=models.CharField(max_length=255, default="")
    stock = models.CharField(max_length=255, default="")

