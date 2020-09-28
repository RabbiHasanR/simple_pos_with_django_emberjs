from django.db import models

from django.conf import settings

User=settings.AUTH_USER_MODEL

class Product(models.Model):
    """A model that contains data for a single product."""
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    title = models.CharField(max_length=255, default="")
    available_inventory = models.PositiveIntegerField(default=0)

