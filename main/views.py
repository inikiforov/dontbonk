from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CalculationForm, ProductForm
from datetime import timedelta
from .calculations import get_estimated_swim_time, total_tri_time, total_nutrition, plan_bike, plan_run, count_list_items, nutrition_planner
from .models import Nutrition
from random import choice
from itertools import chain

def get(self, request):
    form = CalculationForm()
    return render(request, self.template_name)

def home(request):
    #product_form = ProductForm(request.POST)
    #product_form_valid = product_form.is_valid()
    #print(product_form_valid)
    #product_input = product_form.cleaned_data

    form = CalculationForm()
    product_form = ProductForm()

    if request.method == "POST":

        if 'calculate' in request.POST:
            form = CalculationForm(request.POST)

            if form.is_valid():
                input = form.cleaned_data
                result = total_tri_time(input)
                nutrition = total_nutrition(result,input)

                plan_b = {
                    'drink': [],
                    'food': [],
                    'sodium_drink': [],
                    'sodium_food': [],
                    'liquid': 0,
                    'caffene': 0,
                    'carbs': 0,
                    'calories': 0,
                    'sodium': 0,
                }

                plan_r = {
                    'drink': [],
                    'food': [],
                    'sodium_drink': [],
                    'sodium_food': [],
                    'liquid': 0,
                    'caffene': 0,
                    'carbs': 0,
                    'calories': 0,
                    'sodium': 0,
                }

                q_set = Nutrition.objects.all()#.filter(brand_name='Maurten')

                all_drinks = q_set.filter(category='drink')
                random_drink = choice(all_drinks)

                all_food = q_set.filter(category='food')
                random_food = choice(all_food)

                all_sodium_drinks = q_set.filter(category='sodium_drink')
                random_sodium_drink = choice(all_sodium_drinks)
                print(random_sodium_drink)

                sodium_food = q_set.filter(short_name='judees_sodium')
                sodium_food = choice(sodium_food)

                product_set = {
                    'drink': random_drink.simplify(),
                    'food': random_food.simplify(),
                    'sodium_drink': random_sodium_drink.simplify(),
                    'sodium_food': sodium_food.simplify(),
                }
                print(product_set)
                target = {
                    'carbs':int(nutrition[0]),
                    'liquid':int(nutrition[1])
                }

                target_bike = {
                    'carbs': int(nutrition[2]),
                    'liquid': int(nutrition[3]),
                    'sodium': int(nutrition[6]),
                }

                target_run = {
                    'carbs': int(nutrition[4]),
                    'liquid': int(nutrition[5]),
                    'sodium': int(nutrition[7]),
                }

                storage_limits = {
                    'bike_liquid': input['bike_liquid_storage'],
                    'bike_liquid_sodium': 1000,
                    'run_liquid': input['run_liquid_storage']
                }

                print(nutrition[7])
                print(target_run)


                products_bike = plan_bike(plan_b, product_set, target_bike, storage_limits)
                products_run = plan_run(plan_r, product_set, target_run, storage_limits)

                bike_nutrition_list = products_bike['drink']
                bike_nutrition_list.extend(products_bike['food'])
                bike_nutrition_list.extend(products_bike['sodium_drink'])
                bike_nutrition_list.extend(products_bike['sodium_food'])
                bike_nutrition_list_summary = count_list_items(bike_nutrition_list)

                bike_display_set_list = nutrition_planner(bike_nutrition_list_summary, q_set)

                run_nutrition_list = products_run['drink']
                run_nutrition_list.extend(products_run['food'])
                run_nutrition_list.extend(products_run['sodium_drink'])
                run_nutrition_list.extend(products_run['sodium_food'])
                run_nutrition_list_summary = count_list_items(run_nutrition_list)

                run_display_set_list = nutrition_planner(run_nutrition_list_summary, q_set)

                print(run_display_set_list)






        args = {
            'form':form,
            'product_form':product_form,
            'total_time':str(timedelta(seconds = result[0])).split('.')[0],
            'swim_time':str(timedelta(seconds = result[1])).split('.')[0],
            'bike_time':str(timedelta(seconds = result[3])).split('.')[0],
            'run_time':str(timedelta(seconds = result[5])).split('.')[0],
            'carbs_required':int(nutrition[0]),
            'liquid_required':int(nutrition[1]),
            'bike_carbs_target':int(nutrition[2]),
            'bike_liquid_target':int(nutrition[3]),
            'run_carbs_target':int(nutrition[4]),
            'run_liquid_target':int(nutrition[5]),
            'bike_sodium_target': int(nutrition[6]),
            'run_sodium_target': int(nutrition[7]),
            'sodium_required': int(nutrition[8]),
            'bike_display_set_list': bike_display_set_list,
            'run_display_set_list': run_display_set_list,
        }

        return render(request, 'main/home.html', args)



    else:
        form = CalculationForm()
        return render(request, 'main/home.html', {'form': form})

def research(request):
    return render(request, 'main/research.html')

def about(request):
    return render(request, 'main/about.html')