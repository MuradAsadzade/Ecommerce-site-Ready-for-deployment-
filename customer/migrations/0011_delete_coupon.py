# Generated by Django 4.2.1 on 2023-05-25 15:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0010_coupon'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Coupon',
        ),
    ]