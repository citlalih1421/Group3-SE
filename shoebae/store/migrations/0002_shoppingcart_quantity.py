# Generated by Django 5.0.3 on 2024-03-29 03:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoppingcart',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]