from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
import datetime
from purchase.models import PurchaseStatusModel
from collections import defaultdict

month_dict = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August',
              9: 'September', 10: 'October',
              11: 'November', 12: 'December'}

start_datetime = '2019-01-01 17:00'
end_datetime = '2019-12-31 22:00'


def purchase_data(request):
    # FUNCTIONAL BASED VIEW
    global start_datetime, end_datetime

    if request.method == 'GET':
        context = {
            "method": "GET",
            "start": start_datetime,
            "end": end_datetime
        }
        return render(request, 'charts.html', context)
    else:
        start_datetime = ' '.join(request.POST['start'].split('T'))
        end_datetime = ' '.join(request.POST['end'].split('T'))
        context = {
            "method": "POST",
            "start": start_datetime,
            "end": end_datetime
        }
        return render(request, 'charts.html', context)


def check_criteria(temp):
    created_dict = {}

    for i in temp:
        created_dict['id'] = i.purchase_id
        created_dict[i.status] = i.created_at
        created_dict['quantity'] = i.purchase.quantity
    # Chossing date as mentioned
    if created_dict.get('Dispatched') or (created_dict.get('Dispatched') and created_dict.get('Delivered')):
        return {
            'date': created_dict.get('Dispatched'),
            'id': created_dict['id'],
            'quantity': created_dict['quantity']
        }
    if created_dict.get('Delivered'):
        return {
            'date': created_dict.get('Delivered'),
            'id': created_dict['id'],
            'quantity': created_dict['quantity']
        }


def create_data(start_datetime, end_datetime):
    # print(start_datetime, end_datetime)
    try:
        start = start_datetime.split('-')
        start_year = start[0]
        start_month = start[1]
        start_day_time = start[2].split(' ')
        start_day = start_day_time[0]
        start_time = start_day_time[1].split(':')
    except ValueError as e:
        print(e)
    try:
        end = end_datetime.split('-')
        end_year = end[0]
        end_month = end[1]
        end_day_time = end[2].split(' ')
        end_day = end_day_time[0]
        end_time = end_day_time[1].split(':')
    except ValueError as e:
        print(e)
    visited_id = defaultdict(lambda: False)
    data_dict = defaultdict(lambda: 0)
    temp_list = []
    try:
        # Getting the objects depend upon datetime
        all_objects = PurchaseStatusModel.objects.select_related('purchase').filter(
            created_at__gte=datetime.datetime(int(start_year), int(start_month), int(start_day), int(start_time[0]),
                                              int(start_time[1])),
            created_at__lte=datetime.datetime(int(end_year), int(end_month), int(end_day), int(end_time[0]),
                                              int(end_time[1]))).order_by(
            'purchase_id')
    except ConnectionError as e:
        print(e)

    for i in all_objects:
        if not visited_id[i.purchase_id]:
            if temp_list:
                result = check_criteria(temp_list)
                if result:
                    data_dict[result['date'].strftime("%B%Y")] += result['quantity']
                temp_list = []
            temp_list.append(i)
            visited_id[i.purchase_id] = True
        else:
            temp_list.append(i)

    labels = []
    items = []

    months = []

    start_month = int(start_month)
    end_month = int(end_month)
    start_year = int(start_year)
    end_year = int(end_year)
    while (start_month <= end_month) or (start_year <= end_year):
        # Creating the Months with Start / End datetime
        if start_month > 12:
            start_month = 1
            start_year += 1
        if start_year <= end_year:
            months.append(month_dict[start_month]+str(start_year))
            start_month += 1
        else:
            break
    for month in months:
        labels.append(month)
        items.append(data_dict[month])
    data = {
        "labels": labels,
        "default": items,
        "axis": "Quantity"
    }
    return data


class ChartData(APIView):
    # CLASS BASED VIEW
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        data = create_data(start_datetime, end_datetime)
        return Response(data)

    def post(self, request, format=None):
        data = create_data(start_datetime, end_datetime)
        return Response(data)
