from django.db import models


class Product(models.Model):
    """A model that contains data for a single product."""
    price = models.DecimalField(max_digits=8, decimal_places=2)
    title = models.CharField(max_length=255, default="")
    available_inventory = models.PositiveIntegerField(default=0)