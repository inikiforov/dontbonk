from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from .forms import CalculationForm, ProductForm
from datetime import timedelta
from .calculations import get_estimated_swim_time, total_tri_time, total_nutrition, plan_bike, plan_run, count_list_items, nutrition_planner, generate_random_name
from .models import Nutrition, CalculationEntry
from random import choice
from itertools import chain

def get(self, request):
    form = CalculationForm()
    product_form = ProductForm()
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
                print('Showing the input',input)
                print(type(input['food_products']))
                result = total_tri_time(input)
                nutrition = total_nutrition(result,input)

                plan_b = {
                    'drink': [],
                    'food': [],
                    'sodium_drink': [],
                    'sodium_food': [],
                    'water': [],
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
                    'water': [],
                    'liquid': 0,
                    'caffene': 0,
                    'carbs': 0,
                    'calories': 0,
                    'sodium': 0,
                }

                # Создаем списки продуктов для случайного выбора
                q_set = Nutrition.objects.all()#.filter(brand_name='Maurten')

                # Новый код для определения списка продуктов из курируемого списка на основе случайного бренда

                # product_set_cheme: drink, food, sodium_drink, sodium_food, water
                curated_product_set = {
                    'sis': ['sis_beta_80', 'sis_beta_gel', 'skratch_hydration_drink', 'saltstick_fastchews', 'water'],
                    'maurten': ['maurten_drink_320', 'maurten_gel_100', 'skratch_hydration_drink', 'saltstick_fastchews',
                                'water'],
                    'gu' : ['gu_roctane_drink_nocaf', 'gu_roctane_gel','gu_hydro_tabs', 'gu_sodium_caps', 'water']
                }

                base_set = curated_product_set[choice(list(curated_product_set.keys()))]
                #print(base_set)
                base_drink = q_set.get(short_name = base_set[0])
                base_food = q_set.get(short_name=base_set[1])
                base_sodium_drink = q_set.get(short_name=base_set[2])
                base_sodium_food = q_set.get(short_name=base_set[3])
                base_water = q_set.get(short_name=base_set[4])

                base_product_set = {
                    'drink': base_drink.simplify(),
                    'food': base_food.simplify(),
                    'sodium_drink': base_sodium_drink.simplify(),
                    'sodium_food': base_sodium_food.simplify(),
                    'water': base_water.simplify(),
                }

                #print('RANDOM PRODUCT SET', random_product_set)
                print('CURATED PRODUCT SET', base_product_set)

                product_set = {
                    'drink': input['drink_products'],
                    'food': input['food_products'],
                    'sodium_drink': input['sodium_drink_products'],
                    'sodium_food': input['sodium_food_products'],
                    'water': None,
                }


                for i in product_set:
                    if product_set[i] is None:
                        product_set[i] = base_product_set[i]
                    else:
                        product_set[i] = product_set[i].simplify()

                print('Chosen product set',product_set)


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
                bike_nutrition_list.extend(products_bike['water'])
                bike_nutrition_list_summary = count_list_items(bike_nutrition_list)

                bike_display_set_list = nutrition_planner(bike_nutrition_list_summary, q_set)

                run_nutrition_list = products_run['drink']
                run_nutrition_list.extend(products_run['food'])
                run_nutrition_list.extend(products_run['sodium_drink'])
                run_nutrition_list.extend(products_run['sodium_food'])
                run_nutrition_list.extend(products_run['water'])
                run_nutrition_list_summary = count_list_items(run_nutrition_list)

                run_display_set_list = nutrition_planner(run_nutrition_list_summary, q_set)

                print(run_display_set_list)



        print(bike_display_set_list)
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

        random_entry_name = generate_random_name()

        calculation_entry = CalculationEntry(input_data=input, input_products=product_set, calculation_result= args, random_name=random_entry_name, entry_date=timezone.now())
        calculation_entry.save()

        return render(request, 'main/home.html', args)



    else:
        form = CalculationForm()
        product_form = ProductForm()
        return render(request, 'main/home.html', {'form': form,
                                                  'product_form': product_form})

def research(request):
    return render(request, 'main/research.html')

def about(request):
    return render(request, 'main/about.html')