from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Nutrition
from .models import CalculationEntry
from .resource import NutritionResource

#admin.site.register(Nutrition)
admin.site.register(CalculationEntry)

@admin.register(Nutrition)
class NutritionAdmin(ImportExportModelAdmin):
    resource_class = NutritionResource