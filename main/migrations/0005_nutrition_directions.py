# Generated by Django 4.1.3 on 2022-11-21 00:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0004_nutrition_brand_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="nutrition",
            name="directions",
            field=models.TextField(default="None", max_length=200),
        ),
    ]
