# Generated by Django 4.1.3 on 2023-01-22 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0010_alter_calculationentry_entry_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="nutrition",
            name="price",
            field=models.FloatField(blank=True, default=0),
            preserve_default=False,
        ),
    ]
