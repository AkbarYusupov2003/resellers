# Generated by Django 4.1.7 on 2023-07-31 07:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('traffic', '0005_agentorder_created_by'),
    ]

    operations = [
        migrations.RenameField(
            model_name='agentorder',
            old_name='product_group',
            new_name='product_category',
        ),
    ]