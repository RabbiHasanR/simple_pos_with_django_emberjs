from rest_framework import serializers
from .models import Cart,CartItem
from django.conf import settings

from product.serializers import ProductSerializer

User=settings.AUTH_USER_MODEL

# class OrderSerializer(serializers.ModelSerializer):

#     """Serializer for the Product model."""

#     class Meta:
#         model = Order
#         fields = ['id','user','date_ordered', 'complete', 'transaction_id','get_cart_total','get_cart_items','get_order_items']


# class OrderItemSerializer(serializers.ModelSerializer):

#     """Serializer for the Product model."""

#     class Meta:
#         model = OrderItem
#         fields = ['id','product','order', 'quantity', 'date_added']
    
#         def create(self, validated_data):
#             return OrderItem.objects.create(**validated_data)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

class CartSerializer(serializers.ModelSerializer):

    """Serializer for the Cart model."""

    user = UserSerializer(read_only=True)
    # used to represent the target of the relationship using its __unicode__ method
    items = serializers.StringRelatedField(many=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'updated_at','items']
            

class CartItemSerializer(serializers.ModelSerializer):

    """Serializer for the CartItem model."""

    cart = CartSerializer(read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'quantity']

