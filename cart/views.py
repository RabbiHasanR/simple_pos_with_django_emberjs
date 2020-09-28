from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import json

from .serializers import OrderSerializer,OrderItemSerializer
from .models import Order,OrderItem
from product.models import Product


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_cart_item(request,product_id,*args,**kwargs):
    # product_id=request.data['product_id']
    print('product_id:',product_id)
    user=request.user.id
    product=Product.objects.get(id=product_id)
    order,created=Order.objects.get_or_create(user=user,complete=False)
    orderItem,created=OrderItem.objects.get_or_create(product=product,order=order)
    orderItem.quantity= (orderItem.quantity+1)
    serializer=OrderItemSerializer(orderItem)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=200)
    return Response({},status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_cart_item(request,product_id,*args,**kwargs):
    # product_id=request.data['product_id']
    user=request.user.id
    product=Product.objects.get(id=product_id)
    order,created=Order.objects.get_or_create(user=user,complete=False)
    orderItem,created=OrderItem.objects.get_or_create(product=product,order=order)
    if orderItem.quantity>0:
        orderItem.quantity= (orderItem.quantity-1)
    serializer=OrderItemSerializer(orderItem)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=200)
    return Response({},status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cart_items(request,*args,**kwargs):
    user=request.user.id
    order=Order.objects.filter(user=user)
    serailizer=OrderSerializer(order)
    return Response(serailizer.data,status=200)


