# Generated by Django 3.0.5 on 2020-09-15 19:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dieseshop', '0007_order_orderitem'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='ShippingAddress1',
            new_name='shippingAddress1',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='ShippingCity',
            new_name='shippingCity',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='ShippingCountry',
            new_name='shippingCountry',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='ShippingName',
            new_name='shippingName',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='ShippingPostcode',
            new_name='shippingPostcode',
        ),
    ]