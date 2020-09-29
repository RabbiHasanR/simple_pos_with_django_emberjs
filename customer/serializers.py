from rest_framework import serializers
from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):

    """Serializer for the Product model."""

    class Meta:
        model = Customer
        fields = ['id','user','name','phone', 'created_at']
