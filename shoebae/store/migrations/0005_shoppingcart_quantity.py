# Generated by Django 5.0.3 on 2024-04-15 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_cartitem_subtotal_shoppingcart_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoppingcart',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]