# Generated by Django 4.2.13 on 2024-08-29 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("compte", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="photo",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="profile_photo/",
                verbose_name="Photo de profile",
            ),
        ),
    ]
