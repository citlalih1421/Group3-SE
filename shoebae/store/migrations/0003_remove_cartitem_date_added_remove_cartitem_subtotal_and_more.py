# Generated by Django 5.0.3 on 2024-04-07 23:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_shoppingcart_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='date_added',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='subtotal',
        ),
        migrations.RemoveField(
            model_name='shoppingcart',
            name='items',
        ),
        migrations.RemoveField(
            model_name='shoppingcart',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='shoppingcart',
            name='total',
        ),
    ]
