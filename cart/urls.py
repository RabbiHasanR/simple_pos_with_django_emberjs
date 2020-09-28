from django.contrib import admin
from django.urls import path

from .views import (add_cart_item,remove_cart_item,get_cart_items)

'''
CLIENT
base endpoint /api/tweets/
'''

urlpatterns = [
    path('',get_cart_items),
    path('<int:product_id>/add_to_cart/',add_cart_item),
    path('<int:product_id>/remove_to_cart/',remove_cart_item),
]