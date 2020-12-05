import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'assignment.settings')

import django

django.setup()

import random
from purchase.models import PurchaseModel, PurchaseStatusModel
# from collections import defaultdict
from faker import Faker

fakegen = Faker()
import time


def str_time_prop(start, end, format, prop):
    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))


def random_date(start, end, prop):
    return str_time_prop(start, end, '%Y-%m-%d %I:%M', prop)


names = []
for i in range(10):
    names.append(fakegen.name())
print(names)
status = ['Open', 'Verified', 'Dispatched', 'Delivered']
# all_names_avg = defaultdict(lambda : [0,0])
average = 0
for i in range(0, 5000):
    name = random.choice(names)
    if average > 7:
        quantity = random.randint(1, 6)
    else:
        quantity = random.randint(7, 10)
    average = ((average * i) + quantity) / (i + 1)
    obj = PurchaseModel.objects.create(purchaser_name=name, quantity=quantity)
    start_date = "2019-1-1 5:00"
    end_date = "2020-3-31 10:00"
    for status_choice in status:
        print(status_choice)
        random_date_value = random_date(start_date, end_date, random.random())
        start_date = random_date_value
        PurchaseStatusModel.objects.create(purchase=obj, status=status_choice, created_at=random_date_value)


if __name__ == "__main__":
    print("Execution completed")
