# Generated by Django 5.0.3 on 2024-03-18 00:56

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
import mptt.fields
import store.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_name', models.CharField(max_length=100, unique=True)),
                ('brand_logo', models.ImageField(blank=True, null=True, upload_to='images/brands/')),
            ],
        ),
        migrations.CreateModel(
            name='Condition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('condition_name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Shoe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shoe_name', models.CharField(max_length=255)),
                ('shoe_image', models.ImageField(upload_to='images/shoes/')),
                ('shoe_quantity', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('shoe_price', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0.01), django.core.validators.MaxValueValidator(5000), django.core.validators.DecimalValidator(decimal_places=2, max_digits=10)])),
                ('shoe_size', models.DecimalField(decimal_places=1, max_digits=3, validators=[django.core.validators.MinValueValidator(1), django.core.validators.DecimalValidator(decimal_places=1, max_digits=3)])),
                ('shoe_conditions', models.CharField(default='other', max_length=100)),
                ('shoe_brand', models.CharField(default='other', max_length=100)),
                ('shoe_category', models.CharField(default='other', max_length=255)),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=255)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.category')),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_title', models.CharField(max_length=255)),
                ('review_rating', models.DecimalField(decimal_places=1, max_digits=2, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5), django.core.validators.DecimalValidator(decimal_places=1, max_digits=2), store.models.increment_by_half_validator])),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('shoe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.shoe')),
            ],
        ),
    ]
