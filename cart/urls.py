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
    path('',include(router.urls))
]