from django.db import models
import random
import string

class Nutrition(models.Model):
    id = models.BigAutoField(primary_key=True)
    full_name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=100)
    brand_name = models.CharField(max_length=100, default='None')
    drink = models.BooleanField(default=False)
    category = models.CharField(choices=[('drink', 'Drink'), ('food','Food'), ('caffene','Caffene'), ('sodium_drink', 'Sodium Drink'), ('sodium_food', 'Sodium Tabs and Powders'), ('water', 'Water')], max_length=20)
    calories = models.IntegerField()
    carbs = models.IntegerField()
    liquid = models.IntegerField()
    sodium = models.IntegerField(blank=True)
    caffene = models.IntegerField(blank=True)
    price = models.FloatField(blank=True)
    carry_weight = models.FloatField(blank=True)
    directions = models.TextField(max_length=200, default='None')



    def __str__(self):
        return self.full_name

    def simplify(self):
        if self.drink == True:
            return {
                'name': self.short_name,
                'calories': self.calories,
                'carbs': self.carbs,
                'liquid': self.liquid,
                'sodium': self.sodium,
            }
        elif self.drink == False:
            return {
                'name': self.short_name,
                'calories': self.calories,
                'carbs': self.carbs,
                'sodium': self.sodium,
            }

class CalculationEntry(models.Model):
    id = models.BigAutoField(primary_key = True)
    input_data = models.TextField()
    input_products = models.TextField()
    calculation_result = models.TextField()
    random_name = models.CharField(max_length=10, unique=True)
    entry_date = models.DateTimeField()

    def __str__(self):
        return self.random_name

