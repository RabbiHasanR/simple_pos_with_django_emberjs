from rest_framework import serializers
from .models import Order,OrderItem


class OrderSerializer(serializers.ModelSerializer):

    """Serializer for the Product model."""

    class Meta:
        model = Order
        fields = ['id','user','date_ordered', 'complete', 'transaction_id','get_cart_total','get_cart_items','get_order_items']


class OrderItemSerializer(serializers.ModelSerializer):

    """Serializer for the Product model."""

    class Meta:
        model = OrderItem
        fields = ['id','product','order', 'quantity', 'date_added','get_total']

