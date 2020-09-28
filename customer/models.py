from django.db import models

class Customer(models.Model):
    """A model that contains data for a single customer."""
    name = models.CharField(max_length=255, default="")
    phone = models.CharField(max_length=255, default="")
    address = models.CharField(max_length=11, default="")
