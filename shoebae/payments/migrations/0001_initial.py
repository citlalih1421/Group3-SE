# Generated by Django 5.0.3 on 2024-03-29 02:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_holder', models.CharField(blank=True, null=True)),
                ('card_number', models.IntegerField(blank=True, null=True)),
                ('card_expiration', models.DateField(blank=True, null=True)),
                ('card_cvv', models.IntegerField(blank=True, null=True)),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('is_default', models.BooleanField(default=False)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_information', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
