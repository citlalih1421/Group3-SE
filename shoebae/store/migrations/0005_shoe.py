# Generated by Django 5.0.3 on 2024-03-17 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shoe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shoe_name', models.CharField(max_length=255)),
                ('shoe_image', models.ImageField(upload_to='images/shoes/')),
                ('shoe_quantity', models.IntegerField()),
                ('shoe_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('shoe_size', models.DecimalField(decimal_places=1, max_digits=3)),
                ('shoe_conditions', models.CharField(blank=True, choices=[], max_length=100, null=True)),
                ('shoe_brand', models.CharField(blank=True, choices=[], max_length=100, null=True)),
                ('shoe_category', models.CharField(blank=True, choices=[], max_length=255, null=True)),
            ],
        ),
    ]
