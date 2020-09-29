from django.db import models

from django.conf import settings

User=settings.AUTH_USER_MODEL

class Customer(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=255,blank=False)
    phone=models.CharField(max_length=255,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
