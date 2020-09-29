from django.db import models

from customer.models import Customer
from product.models import Product

class Order(models.Model):

    customer = models.ForeignKey(
        Customer,
        related_name='customer',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    total = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class OrderItem(models.Model):
    """A model that contains data for an item in an order."""
    order = models.ForeignKey(
        Order,
        related_name='order',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        related_name='order_product',
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(null=True, blank=True)

    def __unicode__(self):
        return '%s: %s' % (self.product.title, self.quantity)
