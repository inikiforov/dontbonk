# Generated by Django 4.1.3 on 2023-01-21 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0007_alter_nutrition_category"),
    ]

    operations = [
        migrations.CreateModel(
            name="CalculationEntry",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("input_data", models.TextField()),
                ("input_products", models.TextField()),
                ("calculation_result", models.TextField()),
                ("random_name", models.CharField(max_length=10, unique=True)),
                ("entry_date", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
