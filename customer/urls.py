from django.contrib import admin
from django.urls import path

from .views import (customer_create_view,customer_delete_view,customer_details_view,customer_list_view,customer_update_view)

'''
CLIENT
base endpoint /api/tweets/
'''

urlpatterns = [
    path('',customer_list_view),
    path('create/',customer_create_view),
    path('<int:customer_id>/',customer_details_view),
    path('<int:customer_id>/delete/',customer_delete_view),
    path('<int:customer_id>/update/',customer_update_view)
]