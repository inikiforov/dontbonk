from django.db import models

class Nutrition(models.Model):
    id = models.BigAutoField(primary_key=True)
    full_name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=100)
    brand_name = models.CharField(max_length=100, default='None')
    drink = models.BooleanField(default=False)
    category = models.CharField(choices=[('drink', 'Drink'), ('food','Food'), ('caffene','Caffene'), ('sodium_drink', 'Sodium Drink'), ('sodium_tabs', 'Sodium Tabs'), ('water', 'Water')], max_length=20)
    calories = models.IntegerField()
    carbs = models.IntegerField()
    liquid = models.IntegerField()
    sodium = models.IntegerField(blank=True)
    caffene = models.IntegerField(blank=True)
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

