from django.conf.urls import url, include
from rest_framework import routers
from .views import CartViewSet,CartItemViewSet


router = routers.DefaultRouter()
router.register(r'carts', CartViewSet)
router.register(r'cart_items', CartItemViewSet)

urlpatterns = [
    url(r'', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]