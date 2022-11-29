# main/forms.py

#https://simpleisbetterthancomplex.com/article/2017/08/19/how-to-render-django-form-manually.html
#https://simpleisbetterthancomplex.com/tutorial/2018/11/28/advanced-form-rendering-with-django-crispy-forms.html

from django import forms
from.models import Nutrition

class CalculationForm(forms.Form):

    swim_distance = forms.FloatField(label='Swim distance (m)', initial=1900, step_size=100)
    swim_pace = forms.DurationField(label = 'Swim pace (min/100)', initial='2:00')
    bike_distance = forms.FloatField(label = 'Bike distance (km)', initial=70, step_size=1)
    bike_avg_speed = forms.FloatField(label = 'Bike average speed (kph)', initial=35)
    run_distance = forms.FloatField(label = 'Run distance (km)', initial=21.1, step_size=0.1)
    run_pace = forms.DurationField(label = 'Run pace (min/km)', initial='6:00')
    t1_time = forms.DurationField(label = 'Transition 1 time (min)', initial='2:30')
    t2_time = forms.DurationField(label ='Transition 2 time (min)', initial='1:30')
    weight = forms.FloatField(label="Racer's weight (kg)", initial=70, step_size=1)
    carb_rate = forms.IntegerField(label="Carb intake rate (g/hour)", initial=80, step_size=5)
    sweat_rate = forms.IntegerField(label="Sweat rate (ml/hour)", initial=800, step_size=50)
    sodium_rate = forms.IntegerField(label="Sodium loss rate (mg/hour)", initial=600, step_size=50)
    bike_liquid_storage = forms.IntegerField(label = 'Bike liquid storage (ml)', initial=2000, step_size=50)
    run_liquid_storage = forms.IntegerField(label = 'Run liquid storage (ml)', initial=0, step_size=50)
    #test_duration_field = forms.DurationField(label = 'Test duration field', initial='5:00')



class ProductForm(forms.Form):
    drink_products = forms.ModelChoiceField(queryset = Nutrition.objects.filter(drink=True), empty_label='Choose one', required=False)
    food_products = forms.ModelChoiceField(queryset = Nutrition.objects.filter(drink=False), empty_label='Choose one', required=False)
