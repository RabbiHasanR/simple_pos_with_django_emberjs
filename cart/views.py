from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework import status

# from rest_framework.decorators import detail_route
from rest_framework.decorators import action
# from rest_framework.decorators import list_route
from rest_framework.response import Response

from .models import CartItem,Cart
from product.models import Product
from .serializers import CartSerializer,CartItemSerializer


class CartViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows carts to be viewed or edited.
    """
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    @action(detail=True,methods=['post', 'put']) #detail=True,
    def add_to_cart(self, request, pk=None):
        # """Add an item to a user's cart.
        # Adding to cart is disallowed if there is not enough inventory for the
        # product available. If there is, the quantity is increased on an existing
        # cart item or a new cart item is created with that quantity and added
        # to the cart.
        # Parameters
        # ----------
        # request: request
        # Return the updated cart.
        # """
        cart = self.get_object()
        try:
            print('product id:',pk)
            product = Product.objects.get(
                id=pk
            )
            print('products:',product)
            quantity = int(request.data['quantity'])
        except Exception as e:
            print('exception1:',e)
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
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @action(detail=True,methods=['post', 'put']) #detail=True,
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
                id=request.data['product_id']
            )
        except Exception as e:
            print ('exception1:',e)
            return Response({'status': 'fail'})

        try:
            cart_item = CartItem.objects.get(cart=cart,product=product)
        except Exception as e:
            print ('exception2:',e)
            return Response({'status': 'fail'})

        # if removing an item where the quantity is 1, remove the cart item
        # completely otherwise decrease the quantity of the cart item
        if cart_item.quantity == 1:
            cart_item.delete()
        else:
            cart_item.quantity -= 1
            cart_item.save()

        # return the updated cart to indicate success
        serializer = CartSerializer(cart)
        return Response(serializer.data)

class CartItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows cart items to be viewed or edited.
    """
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
