from django.urls import path

from .views import (product_create_view,product_list_view,product_details_view,product_delete_view)

'''
CLIENT
base endpoint /api/tweets/
'''

urlpatterns = [
    path('',product_list_view),
    path('create/',product_create_view),
    path('<int:product_id>/',product_details_view),
    path('<int:product_id>/delete/',product_delete_view)
]