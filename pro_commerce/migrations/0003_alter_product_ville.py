# Generated by Django 4.2.13 on 2024-07-18 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pro_commerce", "0002_alter_category_slug_alter_subcategory_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="ville",
            field=models.CharField(max_length=200, verbose_name="ville du produit"),
        ),
    ]
