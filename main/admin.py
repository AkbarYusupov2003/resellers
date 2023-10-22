from django.contrib import admin

from main import models


admin.site.register(models.Warehouse)
admin.site.register(models.Product)
admin.site.register(models.ProductCategory)
admin.site.register(models.Stock)
