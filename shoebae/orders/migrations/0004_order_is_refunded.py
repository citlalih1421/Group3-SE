# Generated by Django 5.0.3 on 2024-04-08 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_rename_orderitem_order_items_order_shippinginfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_refunded',
            field=models.BooleanField(default=False),
        ),
    ]