from django.contrib import admin
from django.urls import path,include
from rest_framework import routers

from .views import (CartViewSet,CartItemViewSet)

'''
CLIENT
base endpoint /api/tweets/
'''
router = routers.DefaultRouter()
router.register(r'carts', CartViewSet)
router.register(r'cart_items',CartItemViewSet)

urlpatterns = [
    # path('',get_cart_items),
    # path('add_to_cart/<int:product_id>/',cart_item_add_view),
    # path('<int:product_id>/remove_to_cart/',cart_item_remove_view),
    path('',include(router.urls))
]