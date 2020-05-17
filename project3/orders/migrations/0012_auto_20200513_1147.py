# Generated by Django 3.0.3 on 2020-05-13 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0011_auto_20200513_1102'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='itemID',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='orderID',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='toppingID',
        ),
        migrations.RenameField(
            model_name='cart',
            old_name='userID',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='cartitem',
            old_name='cartID',
            new_name='cart',
        ),
        migrations.RenameField(
            model_name='cartitem',
            old_name='itemID',
            new_name='item',
        ),
        migrations.RenameField(
            model_name='cartitem',
            old_name='toppingID',
            new_name='topping',
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='size',
            field=models.CharField(choices=[('Small', 'Small'), ('Large', 'Large')], max_length=7),
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='OrderItem',
        ),
    ]
