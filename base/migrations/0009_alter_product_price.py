# Generated by Django 4.1 on 2022-08-23 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
    ]
