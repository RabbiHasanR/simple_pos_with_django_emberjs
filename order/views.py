from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from django.db.models import FloatField
from django.db.models import F
from django.db.models import Sum

from .models import OrderItem,Order
from customer.models import Customer

from .serializers import OrderItemSerializer,OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows orders to be viewed or created.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


    def perform_create(self, serializer):
        try:
            purchaser_id = self.request.data['customer']
            customer = Customer.objects.get(pk=purchaser_id)
        except:
            raise serializers.ValidationError(
                'User was not found'
            )

        cart = customer.cart

        for cart_item in cart.items.all():
            if cart_item.product.available_inventory - cart_item.quantity < 0:
                raise serializers.ValidationError(
                    'We do not have enough inventory of ' + str(cart_item.product.title) + \
                    'to complete your purchase. Sorry, we will restock soon'
                )

        # find the order total using the quantity of each cart item and the product's price
        total_aggregated_dict = cart.items.aggregate(total=Sum(F('quantity')*F('product__price'),output_field=FloatField()))

        order_total = round(total_aggregated_dict['total'], 2)
        order = serializer.save(customer=customer, total=order_total)

        order_items = []
        for cart_item in cart.items.all():
            order_items.append(OrderItem(order=order, product=cart_item.product, quantity=cart_item.quantity))
            # available_inventory should decrement by the appropriate amount
            cart_item.product.available_inventory -= cart_item.quantity
            cart_item.product.save()


        OrderItem.objects.bulk_create(order_items)
        cart.items.clear()

    def create(self, request, *args, **kwargs):
        """Override the creation of Order objects.
        Parameters
        ----------
        request: dict
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False,url_path="order_history/(?P<customer_id>[0-9])")
    def order_history(self, request, customer_id):
        """Return a list of a user's orders.
        Parameters
        ----------
        request: request
        """
        try:
            customer = Customer.objects.get(id=customer_id)

        except:
            # no user was found, so order history cannot be retrieved.
            return Response({'status': 'fail'})

        orders = Order.objects.filter(customer=customer)
        serializer = OrderSerializer(orders, many=True)

        return Response(serializer.data)


class OrderItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows order items to be viewed or edited.
    """
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
