# from meal.models import Meal,Category
# import urllib.request, json 
# import random
# with open('foods.json') as json_file:
#     data = json.load(json_file)
 
#     # Print the type of data variable
#     for item in data['foodItems']:
#         Meal(category=random.choice(Category.objects.all()),name=item['foodName'],price=round(random.uniform(0.50, 3.50), 2),calories = item['calories']).save()
# #category = random.choice(Category.objects.all())
# #print(round(random.uniform(0.50, 3.50), 2))

from datetime import datetime,timedelta
d1 = datetime.now()-timedelta(days=2,hours=3)
print((datetime.now()-d1).days)