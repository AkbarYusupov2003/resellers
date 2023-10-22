from django.conf import settings
from django.db import models

from company.models import Company


class Warehouse(models.Model):
    owner = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="warehouses"
    )
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
    )
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=512)

    def __str__(self):
        return self.name


class Product(models.Model):
    supplier = models.ForeignKey("traffic.Supplier", on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    description = models.TextField(max_length=1024, null=True, blank=True)
    category = models.ForeignKey(
        "ProductCategory", null=True, on_delete=models.SET_NULL
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ProductCategory(models.Model):
    owner = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Product Categories"


class Stock(models.Model):

    class CurrencyChoices(models.IntegerChoices):
        sum = 1, "sum"
        dollar = 2, "dolar"

    # dona, qop, korobka, litr, pachka, shunga oxshash
    product = models.ForeignKey(
        Product, null=True, on_delete=models.SET_NULL
    )
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    purchase_price = models.PositiveIntegerField()
    currency = models.PositiveSmallIntegerField(
        choices=CurrencyChoices.choices, default=1
    )
    quantity = models.PositiveIntegerField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.category.name}, {self.quantity}та {self.product.name}, {self.purchase_price} {self.get_currency_display()}"
