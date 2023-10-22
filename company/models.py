from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, m2m_changed
from django.dispatch import receiver


class Company(models.Model):
    admins = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="company_admin"
    )
    # company_warehouseman
    agents = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="company_agents"
    )
    name = models.CharField(max_length=255)
    email = models.EmailField()
    address = models.CharField(max_length=512)
    phone_number = models.CharField(max_length=16)
    license_number = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def admins_counter(self):
        return self.admins.all().count()

    def agents_counter(self):
        return self.agents.all().count()

    class Meta:
        verbose_name_plural = "Companies"
