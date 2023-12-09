from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from inventories.models import Inventory
from products.models import Product, ProductType
from vehicles.models import Vehicle
from person.models import Person
from destinations.models import Destination
import json
import pandas as pd
import numpy as np
import datetime
from django.db.models import Q

# Create your views here.
def report(request):
    products = Product.objects.all()
    product_types = ProductType.objects.all()
    vehicles = Vehicle.objects.all()
    drivers = Person.objects.filter(type='driver')
    suppliers = Person.objects.filter(type='supplier')
    destinations = Destination.objects.all()
    customers = Person.objects.filter(type='customer')
    context = {
        'products': products,
        'product_types': product_types,
        'vehicles': vehicles,
        'drivers': drivers,
        'suppliers': suppliers,
        'destinations': destinations,
        'customers': customers,
    }

    return render(request, 'report.html', context)

# Generate report using pandas
def report_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            start_date = data.get('start_date')
            end_date = data.get('end_date')
            group_by = data.get('group_by')
            column_filter = data.get('column_filter')
            order = data.get('order')
            filter_obj = data.get('filter_obj')

            #print([start_date, end_date, group_by, column_filter])
            #print(filter_obj)

            # if not all([start_date, end_date, group_by]):
            #     return JsonResponse({'message': 'Missing required parameters'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data'}, status=400)

        try:
            #print('start query')
            inventories = Inventory.objects.select_related('vehicle', 'driver', 'supplier', 'customer', 'product')
            # filter date range
            if start_date and end_date:
                inventories = inventories.filter(date__range=[start_date, end_date])
            elif start_date:
                inventories = inventories.filter(date__gte=start_date)
            elif end_date:
                inventories = inventories.filter(date__lte=end_date)


            if filter_obj:
                if filter_obj['product']:
                    # exclude product
                    inventories = inventories.exclude(product__code__in=filter_obj['product'])
                if filter_obj['customer']:
                    # exclude customer
                    inventories = inventories.exclude(customer__code__in=filter_obj['customer'])
                if filter_obj['supplier']:
                    # exclude supplier
                    inventories = inventories.exclude(supplier__code__in=filter_obj['supplier'])
                if filter_obj['driver']:
                    # exclude driver
                    inventories = inventories.exclude(driver__code__in=filter_obj['driver'])
                if filter_obj['vehicle']:
                    # exclude vehicle
                    inventories = inventories.exclude(vehicle__reg_no__in=filter_obj['vehicle'])



            df = pd.DataFrame(list(inventories.values(
                'id', 'date', 
                'vehicle__reg_no', 'vehicle__model', 'driver__code', 'driver__name', 
                'supplier__code', 'supplier__name', 'supplier_qty',
                'customer__code', 'customer__name', 
                'product__code', 'product__name', 
                'ticket_no', 'do', 'weight_in', 'weight_out', 'deduction', 'remark', 'customer_ticket_no', 
                'factory_nett', 'bucket'
            )))
            #print(df.columns)
            convert_dict = {
                'id': int,
                'date': str,
                'vehicle__reg_no': str,
                'vehicle__model': str,
                'driver__code': 'category',
                'driver__name': 'category',
                'supplier__code': 'category', 
                'supplier__name': 'category',
                'supplier_qty': int,
                'customer__code': 'category',
                'customer__name': 'category',
                'product__code': 'category',
                'product__name': 'category',
                'ticket_no': str,
                'do': str,
                'weight_in': int,
                'weight_out': int,
                'deduction': int,
                'remark': str,
                'customer_ticket_no': str,
                'factory_nett': int,
                'bucket': float
            }
            

            df = df.astype(convert_dict)
            print(df.columns)
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            df['weight_nett'] = df['weight_in'] - df['weight_out'] - df['deduction']   
                 

            json_data = generate_report(df, start_date, end_date, group_by, column_filter, order, filter_obj)
            return JsonResponse({'message': 'Success', 'report_data': json_data}, status=200)
        except Exception as e:
            return JsonResponse({'message': 'Error processing data', 'error': str(e)}, status=500)

    return HttpResponseBadRequest('Method not allowed')

def generate_report(data, start, end, group_by, filter, order, filter_obj):
    code_suffix, name_suffix = '__code', '__name'
    if group_by == 'vehicle':
        code_suffix, name_suffix = '__reg_no', '__model'
    group_name = group_by+name_suffix if group_by else None
    group_by = group_by+code_suffix if group_by else None
    #print({'start': start, 'end': end, 'group_by': group_by, 'filter': filter})

    try:        
        report = data
        report = report[order]

        if group_by is not None:
            group = report.groupby(group_by)['weight_nett'].sum()
            report = report.sort_values(by=group_by, ascending=True)
            totals_df = pd.DataFrame({group_by: group.index, 'weight_nett': group.values, 'remark': 'Total'})
            report = pd.concat([report, totals_df])
            
            report = report.sort_values(by=[group_by, 'date'], ascending=True, na_position='last')
            report = report.reset_index(drop=True)

            cols = [group_by, group_name] + [col for col in order if col not in [group_by, group_name]]
            report = report[cols]
            # remove column in filter array
            #print(filter)

        report = report.drop(columns=filter)
        report['date'] = report['date'].dt.date
        report['date'] = report['date'].astype(str)
        return report.to_json(orient='index')
    except Exception as e:
        print(e)
        raise Exception('Error generating report: ' + str(e))


grouping = ['product', 'driver', 'supplier', 'destination', 'vehicle']