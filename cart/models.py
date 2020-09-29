from django.db import models
from product.models import Product
from django.conf import settings
User=settings.AUTH_USER_MODEL

# class Order(models.Model):
# 	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
# 	date_ordered = models.DateTimeField(auto_now_add=True)
# 	complete = models.BooleanField(default=False)
# 	transaction_id = models.CharField(max_length=100, null=True)

# 	def __str__(self):
# 		return str(self.id)

# 	@property
# 	def get_order_items(self):
# 		all_oreder_items = self.orderitem_set.all()
# 		return all_oreder_items 

# 	@property
# 	def get_cart_total(self):
# 		orderitems = self.orderitem_set.all()
# 		total = sum([item.get_total for item in orderitems])
# 		return total 

# 	@property
# 	def get_cart_items(self):
# 		orderitems = self.orderitem_set.all()
# 		total = sum([item.quantity for item in orderitems])
# 		return total 
        

# class OrderItem(models.Model):
# 	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
# 	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
# 	quantity = models.IntegerField(default=0, null=True, blank=True)
# 	date_added = models.DateTimeField(auto_now_add=True)


# 	@property
# 	def get_total(self):
# 		total = self.product.price * self.quantity
# 		return total


class Cart(models.Model):
    """A model that contains data for a shopping cart."""
    user = models.OneToOneField(
        User,
        related_name='user',
		on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CartItem(models.Model):
    """A model that contains data for an item in the shopping cart."""
    cart = models.ForeignKey(
        Cart,
        related_name='cart',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    product = models.ForeignKey(
        Product,
        related_name='product',
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1, null=True, blank=True)

    # def __unicode__(self):
    #     return '%s: %s' % (self.product.title, self.quantity)
