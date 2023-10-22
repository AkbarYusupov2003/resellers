from django.conf import settings
from django.db import models

from company.models import Company
from main.models import Warehouse, ProductCategory


class Supplier(models.Model):
    owner = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="suppliers"
    )
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=512)
    phone_number = models.CharField(max_length=16)
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Transfer(models.Model):
    owner = models.ForeignKey(Company, on_delete=models.CASCADE)
    source = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE,
        related_name="transfer_source"
    )
    destination = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE,
        related_name="transfer_destination"
    )
    info = models.TextField(max_length=1024)
    # ↓ Stocks data field  ↓
    data = models.TextField()
    transferred_at = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    owner = models.ForeignKey(Company, on_delete=models.CASCADE)
    source = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE,
        related_name="order_source"
    )
    # ↓ Stocks data field  ↓
    data = models.TextField()
    customer_name = models.CharField(max_length=255)
    customer_address = models.CharField(max_length=512)
    customer_phone = models.CharField(max_length=16)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.data


class AgentOrder(models.Model):
    owner = models.ForeignKey(Company, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    product_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    description = models.TextField(max_length=1024, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
