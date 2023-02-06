from import_export import resources
from .models import Nutrition

class NutritionResource(resources.ModelResource):
    class Meta:
        model = Nutrition
        fields = ('id', 'full_name', 'short_name', 'brand_name', 'drink', 'category', 'calories', 'carbs', 'liquid', 'sodium', 'caffene', 'price', 'carry_weight', 'directions')
