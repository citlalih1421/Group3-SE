# Generated by Django 5.0.3 on 2024-03-28 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoe',
            name='slug',
            field=models.SlugField(default=0, unique=True),
        ),
    ]
