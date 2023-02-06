from datetime import timedelta
from .models import Nutrition, CalculationEntry
import random
import string



def get_estimated_swim_time(swim_pace, swim_distance):
    #pace_list = swim_pace.split(':')
    #pace_td = timedelta(minutes=int(pace_list[0]),seconds=int(pace_list[1]))
    #return (swim_distance/100)*pace_td.seconds
    return ((swim_distance/100)*swim_pace).seconds

def get_estimated_bike_time(bike_avg_speed, bike_distance):
    return (bike_distance/bike_avg_speed)*60*60

def get_estimated_run_time(run_pace, run_distance):
    #pace_list = run_pace.split(':')
    #pace_td = timedelta(minutes=int(pace_list[0]),seconds=int(pace_list[1]))
    #return run_distance*pace_td.seconds
    return run_distance*run_pace

def get_estimated_transition_time(t_time):
    time_list = t_time.split(':')
    time_td = timedelta(minutes=int(time_list[0]),seconds=int(time_list[1]))
    return time_td.seconds

def get_total_tri_race_time(swim_time, t1_time, bike_time, t2_time, run_time):
    l = [swim_time, t1_time, bike_time, t2_time, run_time]
    l.append(sum(l))
    return


# функция получит на вход вот такой dict
# {'swim_distance': 3200.0, 'swim_pace': datetime.timedelta(seconds=120), 'bike_distance': 70.0, 'bike_avg_speed': '35', 'run_distance': 21.1, 'run_pace': datetime.timedelta(seconds=360), 't1_time': datetime.timedelta(seconds=150), 't2_time': datetime.timedelta(seconds=90)}
# нужно выдать стринг с результатами типа got_total_tri_race_time

def total_tri_time(input):
    swim_time = ((input['swim_distance']/100)*input['swim_pace']).seconds
    bike_time = (input['bike_distance']/input['bike_avg_speed'])*60*60
    run_time = (input['run_distance']*input['run_pace']).seconds
    t1_time = 0
    t2_time = 0
    return [swim_time+bike_time+run_time,swim_time, t1_time, bike_time, t2_time, run_time]

'''
def total_nutrition_old(timing_list, weight):
    carbs_required = 75 #grams per hour
    calories_required = 300 #kcal per hour
    liquid_required = 10*weight*0.034*30 #ml per hour
    total_carbs = (carbs_required/60/60)*timing_list[0]
    total_calories = (calories_required/60/60)*timing_list[0]
    total_liquid = (liquid_required/60/60)*timing_list[0]
    return [total_carbs, total_calories, total_liquid]
'''

def total_nutrition(timing_list, input):
    bike_carb_rate = input['carb_rate']
    bike_liquid_rate = input['sweat_rate']
    run_carb_rate = input['carb_rate']
    run_liquid_rate = input['sweat_rate']
    sodium_rate = input['sodium_rate']*(input['sweat_rate']/1000)
    bike_sodium_rate = input['sodium_rate']*(input['sweat_rate']/1000)
    run_sodium_rate = input['sodium_rate']*(input['sweat_rate']/1000)
    bike_carbs_target = (bike_carb_rate/60/60)*timing_list[3]
    bike_liquid_target = (bike_liquid_rate/60/60)*timing_list[3]
    bike_sodium_target = (bike_sodium_rate/60/60)*timing_list[3]
    run_carbs_target = (run_carb_rate / 60 / 60) * timing_list[5]
    run_liquid_target = (run_liquid_rate / 60 / 60) * timing_list[5]
    run_sodium_target = (run_sodium_rate/60/60)*timing_list[5]
    total_carbs = bike_carbs_target+run_carbs_target
    total_liquid = bike_liquid_target+run_liquid_target
    total_sodium = bike_sodium_target+run_sodium_target
    return [total_carbs, total_liquid, bike_carbs_target, bike_liquid_target, run_carbs_target, run_liquid_target, bike_sodium_target, run_sodium_target, total_sodium]

def add_serving(plan, category, product):
    for i in product:
        if isinstance(product[i], int):
            plan[i] = plan[i]+product[i]
        elif i == 'name':
            plan[category].append(product[i])
            print(product[i], 'added to plan')

    return plan


def plan_bike(plan, product_set, target, storage_limits):
    #load carbs while checking not to exceed liquid storage limit
    while plan['carbs'] + product_set['drink']['carbs'] <= target['carbs'] and plan['liquid'] + product_set['drink']['liquid'] <= storage_limits['bike_liquid']:
        add_serving(plan, 'drink', product_set['drink'])
    #load additional carbs - gels that dont require liquid carry capacity
    while plan['carbs'] + product_set['food']['carbs'] <= target['carbs']:
        add_serving(plan, 'food', product_set['food'])
    #if you have space liquid capacity attempt to fill it with electrolyte drink
    ##doesnt check for space carbs capacity. Some electrolyte drinks in database have non insignificant amount of carbs
    while plan['liquid'] + product_set['sodium_drink']['liquid'] <= target['liquid'] and plan['sodium'] + product_set['sodium_drink']['sodium'] <= target['sodium'] and plan['liquid'] + product_set['sodium_drink']['liquid'] <= storage_limits['bike_liquid']:
        add_serving(plan, 'sodium_drink', product_set['sodium_drink'])
    #add sodium suplements that can be mixed in existing liquid or taken without liquid
    while plan['sodium'] + product_set['sodium_food']['sodium'] <= target['sodium']:
        add_serving(plan, 'sodium_food', product_set['sodium_food'])
    #add course water
    while plan['liquid'] + product_set['water']['liquid'] <= target['liquid']:
        add_serving(plan, 'water', product_set['water'])

    return plan

def plan_run(plan, product_set, target, storage_limits):
    while plan['carbs'] + product_set['drink']['carbs'] <= target['carbs'] and plan['liquid'] + product_set['drink']['liquid'] <= storage_limits['run_liquid']:
        add_serving(plan, 'drink', product_set['drink'])

    while plan['carbs'] + product_set['food']['carbs'] <= target['carbs']:
        add_serving(plan, 'food', product_set['food'])

    while plan['sodium'] + product_set['sodium_food']['sodium'] <= target['sodium']:
        add_serving(plan, 'sodium_food', product_set['sodium_food'])

    while plan['liquid'] + product_set['water']['liquid'] <= target['liquid']:
        add_serving(plan, 'water', product_set['water'])

    return plan

def count_list_items(l):
    result = []
    output = []
    for i in l:
        if i not in result:
            result.append(i)
    for i in result:
        output.append([i, l.count(i)])
    return output

def random_item(model,key):
    subset = list(model.objects.get(category=key))
    return random.choice(subset)


def nutrition_planner(nutrition_list, q_set):
    #pass
    output = []
    #input form: [['maurten_drink', 4], ['maurten_gel', 2]]
    #needs to output list of dicts with all relevant information for display

    for i in nutrition_list:
        product = q_set.filter(short_name=i[0])
        #print('This is what i want:', bike_display_set)
        product_with_ammounts = {
            'id': product[0].id,
            'full_name': product[0].full_name,
            'short_name': product[0].short_name,
            'brand_name': product[0].brand_name,
            'carbs': product[0].carbs,
            'calories': product[0].calories,
            'category': product[0].category,
            'ammount': i[1],
            'liquid': product[0].liquid,
            'sodium': product[0].sodium,

        }
        output.append(product_with_ammounts)
    total = {
        'full_name': 'Total',
        'carbs': 0,
        'calories': 0,
        'amount': 0,
        'liquid': 0,
        'sodium': 0,
    }
    for i in output:
        total['carbs'] += i['carbs'] * i['ammount']
        total['calories'] += i['calories'] * i['ammount']
        total['sodium'] += i['sodium'] * i['ammount']
        total['liquid'] += i['liquid'] * i['ammount']
        total['amount'] += i['ammount']

    output.append(total)
    return output

def generate_random_name():
    random_name = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    while CalculationEntry.objects.filter(random_name=random_name).exists():
        random_name = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

    print('New random name is:', random_name)
    return random_name