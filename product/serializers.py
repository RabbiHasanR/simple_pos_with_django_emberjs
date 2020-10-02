from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):

    """Serializer for the Product model."""

    class Meta:
        model = Product
        fields = ['id','title','price', 'category', 'stock']
