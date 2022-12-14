# Generated by Django 4.1.3 on 2022-11-22 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0005_nutrition_directions"),
    ]

    operations = [
        migrations.AlterField(
            model_name="nutrition",
            name="category",
            field=models.CharField(
                choices=[
                    ("drink", "Drink"),
                    ("food", "Food"),
                    ("caffene", "Caffene"),
                    ("sodium_drink", "Sodium Drink"),
                    ("sodium_tabs", "Sodium Tabs"),
                    ("water", "Water"),
                ],
                max_length=20,
            ),
        ),
    ]
