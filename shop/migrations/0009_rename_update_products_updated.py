# Generated by Django 4.2.1 on 2023-06-03 12:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_products_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='products',
            old_name='update',
            new_name='updated',
        ),
    ]