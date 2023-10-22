from django.contrib import admin

from traffic import models


admin.site.register(models.Supplier)
admin.site.register(models.Transfer)
admin.site.register(models.Order)
admin.site.register(models.AgentOrder)
