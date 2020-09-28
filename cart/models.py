from django.db import models
from product.models import Product

# Create your models here.

class Cart(models.Model):
    """A model that contains data for a shopping cart."""
    # customer = models.OneToOneField(
    #     settings.AUTH_USER_MODEL,
    #     related_name='cart'
    # )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CartItem(models.Model):
    """A model that contains data for an item in the shopping cart."""
    cart = models.ForeignKey(
        Cart,
        related_name='items',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    product = models.ForeignKey(
        Product,
        related_name='items',
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1, null=True, blank=True)
