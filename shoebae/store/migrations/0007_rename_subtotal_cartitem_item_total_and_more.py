# Generated by Django 5.0.3 on 2024-04-24 19:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_remove_shoppingcart_quantity'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartitem',
            old_name='subtotal',
            new_name='item_total',
        ),
        migrations.RenameField(
            model_name='shoppingcart',
            old_name='total',
            new_name='cart_total',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='shopping_cart',
        ),
        migrations.AddField(
            model_name='cartitem',
            name='item_quantity',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='shoe',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cart_item', to='store.shoe'),
        ),
        migrations.AlterField(
            model_name='shoppingcart',
            name='customer',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='shopping_cart', to=settings.AUTH_USER_MODEL),
        ),
    ]
