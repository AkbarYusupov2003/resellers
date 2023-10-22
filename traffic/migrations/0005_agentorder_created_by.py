# Generated by Django 4.1.7 on 2023-07-31 07:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('traffic', '0004_rename_customer_agentorder_supplier'),
    ]

    operations = [
        migrations.AddField(
            model_name='agentorder',
            name='created_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
