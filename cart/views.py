from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers

# Create your views here.
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action

from .serializers import CartSerializer,CartItemSerializer
from .models import Cart,CartItem
from product.models import Product


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def cart_item_add_view(request,product_id,*args,**kwargs):
#     # product_id=request.data['product_id']
#     print('product_id:',product_id)
#     user=request.user
#     #product=Product.objects.get(id=product_id)
#     order,created=Order.objects.get_or_create(user=user,complete=False)
#     orderItem,created=OrderItem.objects.get_or_create(product=product_id,order=order)
#     orderItem.quantity= (orderItem.quantity+1)
#     #orderItem.save()
#     # request.data['product']=product
#     # request.data['order']=order
#     # request.data['quantity']=quantity
#     # serialized_obj = serializers.serialize('json', [orderItem, ])
#     # return JsonResponse(serialized_obj,safe=False)
#     # print(orderItem)
#     serializer=OrderItemSerializer(data=orderItem)
#     if serializer.is_valid():
#         serializer.save()
#         print(serializer.data)
#         return Response(serializer.data,status=200)
#     return Response({},status=400)


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def cart_item_remove_view(request,product_id,*args,**kwargs):
#     # product_id=request.data['product_id']
#     user=request.user.id
#     product=Product.objects.get(id=product_id)
#     order,created=Order.objects.get_or_create(user=user,complete=False)
#     orderItem,created=OrderItem.objects.get_or_create(product=product,order=order)
#     if orderItem.quantity>0:
#         orderItem.quantity= (orderItem.quantity-1)
#     serializer=OrderItemSerializer(orderItem)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data,status=200)
#     return Response({},status=400)

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_cart_items(request,*args,**kwargs):
#     user=request.user.id
#     order=Order.objects.filter(user=user)
#     serailizer=OrderSerializer(order)
#     return Response(serailizer.data,status=200)


class CartViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows carts to be viewed or edited.
    """
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    @action(detail=True,methods=['POST', 'PUT'])
    def add_to_cart(self, request, pk=None):
        """Add an item to a user's cart.
        Adding to cart is disallowed if there is not enough inventory for the
        product available. If there is, the quantity is increased on an existing
        cart item or a new cart item is created with that quantity and added
        to the cart.
        Parameters
        ----------
        request: request
        Return the updated cart.
        """
        cart = self.get_object()
        try:
            product = Product.objects.get(
                pk=request.data['product_id']
            )
            quantity = int(request.data['quantity'])
        except Exception as e:
            print (e)
            return Response({'status': 'fail'})

        # Disallow adding to cart if available inventory is not enough
        if product.available_inventory <= 0 or product.available_inventory - quantity < 0:
            print ("There is no more product available")
            return Response({'status': 'fail'})

        existing_cart_item = CartItem.objects.filter(cart=cart,product=product).first()
        # before creating a new cart item check if it is in the cart already
        # and if yes increase the quantity of that item
        if existing_cart_item:
            existing_cart_item.quantity += quantity
            existing_cart_item.save()
        else:
            new_cart_item = CartItem(cart=cart, product=product, quantity=quantity)
            new_cart_item.save()

        # return the updated cart to indicate success
        serializer = CartSerializer(data=cart)
        return Response(serializer.data,status=200)

    @action(detail=True,methods=['POST', 'PUT'])
    def remove_from_cart(self, request, pk=None):
        """Remove an item from a user's cart.
        Like on the Everlane website, customers can only remove items from the
        cart 1 at a time, so the quantity of the product to remove from the cart
        will always be 1. If the quantity of the product to remove from the cart
        is 1, delete the cart item. If the quantity is more than 1, decrease
        the quantity of the cart item, but leave it in the cart.
        Parameters
        ----------
        request: request
        Return the updated cart.
        """
        cart = self.get_object()
        try:
            product = Product.objects.get(
                pk=request.data['product_id']
            )
        except Exception as e:
            print (e)
            return Response({'status': 'fail'})

        try:
            cart_item = CartItem.objects.get(cart=cart,product=product)
        except Exception as e:
            print (e)
            return Response({'status': 'fail'})

        # if removing an item where the quantity is 1, remove the cart item
        # completely otherwise decrease the quantity of the cart item
        if cart_item.quantity == 1:
            cart_item.delete()
        else:
            cart_item.quantity -= 1
            cart_item.save()

        # return the updated cart to indicate success
        serializer = CartSerializer(data=cart)
        return Response(serializer.data)

class CartItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows cart items to be viewed or edited.
    """
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

