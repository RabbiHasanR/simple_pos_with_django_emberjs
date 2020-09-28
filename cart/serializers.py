from rest_framework import serializers
from .models import Cart,CartItem
from product.serializers import ProductSerializer

class CartSerializer(serializers.ModelSerializer):

    """Serializer for the Cart model."""

    # customer = UserSerializer(read_only=True)
    # used to represent the target of the relationship using its __unicode__ method
    items = serializers.StringRelatedField(many=True)

    class Meta:
        model = Cart
        fields = (
            'id', 'created_at', 'updated_at', 'items'
        ) #, 'customer'

class CartItemSerializer(serializers.ModelSerializer):

    """Serializer for the CartItem model."""

    cart = CartSerializer(read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = (
            'id', 'cart', 'product', 'quantity'
        )
