# Generated by Django 5.0.3 on 2024-03-17 00:57

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_usertype_delete_groupprofile'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Buyer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': [('can_view_buyer', 'Can view buyer'), ('can_edit_buyer', 'Can edit buyer')],
            },
        ),
        migrations.CreateModel(
            name='PaymentInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_holder', models.CharField(blank=True, null=True)),
                ('card_number', models.BinaryField(blank=True, null=True)),
                ('card_expiration', models.BinaryField(blank=True, null=True)),
                ('card_cvv', models.BinaryField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': [('can_view_seller', 'Can view seller'), ('can_edit_seller', 'Can edit seller')],
            },
        ),
        migrations.CreateModel(
            name='ShippingInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.BinaryField(blank=True, null=True)),
                ('city', models.BinaryField(blank=True, null=True)),
                ('zipcode', models.BinaryField(blank=True, null=True)),
                ('state', models.BinaryField(blank=True, null=True)),
                ('country', models.BinaryField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentMethods',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_default_payment', models.BooleanField(default=False)),
                ('payment_info', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounts.paymentinfo')),
            ],
        ),
        migrations.CreateModel(
            name='ShippingMethods',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_default_shipping', models.BooleanField(default=False)),
                ('shipping_info', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounts.shippinginfo')),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_buyer', models.BooleanField(default=True)),
                ('is_seller', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this customer belongs to. A customer will get all permissions granted to each of their groups', related_name='customer_set', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this customer', related_name='customer_set', to='auth.permission', verbose_name='user permissions')),
                ('payment_methods', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounts.paymentmethods')),
                ('shipping_methods', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounts.shippingmethods')),
            ],
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.DeleteModel(
            name='UserType',
        ),
    ]
