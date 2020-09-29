from django.contrib import admin
from django.urls import path,include
from rest_framework import routers
from .views import (OrderViewSet,OrderItemViewSet)

router = routers.DefaultRouter()
router.register(r'orders', OrderViewSet)
router.register(r'order_items', OrderItemViewSet)

# Wire up the API using automatic URL routing
urlpatterns = [
    path('', include(router.urls)),
]