# Generated by Django 4.2.5 on 2023-09-13 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_alter_product_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_favorite',
            field=models.BooleanField(default=False),
        ),
    ]
