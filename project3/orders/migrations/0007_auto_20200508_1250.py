# Generated by Django 3.0.3 on 2020-05-08 16:50

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0006_auto_20200508_1249'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Orders',
            new_name='Order',
        ),
        migrations.RenameModel(
            old_name='OrderItems',
            new_name='OrderItem',
        ),
        migrations.RenameModel(
            old_name='Toppings',
            new_name='Topping',
        ),
    ]
