from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Inventory
from products.models import Product
from vehicles.models import Vehicle
from person.models import Person
from destinations.models import Destination
import json
from datetime import datetime, date
import calendar

# Create your views here.
@login_required(login_url='login')
def inventories(request):
    #inventories = Inventory.objects.all()
    products = Product.objects.all()
    vehicles = Vehicle.objects.all()
    drivers = Person.objects.filter(type='driver')
    suppliers = Person.objects.filter(type='supplier')
    customers = Person.objects.filter(type='customer')
    destinations = Destination.objects.all()
    current_date = datetime.now()

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        inventories = Inventory.objects.filter(date__range=[start_date, end_date])

        context = {
            'inventories': inventories,
            'products': products,
            'vehicles': vehicles,
            'drivers': drivers,
            'suppliers': suppliers,
            'customers': customers,
            'destinations': destinations,
            'start_date': start_date,
            'end_date': end_date,
        }
        return render(request, 'inventory.html', context)



    # Calculate the start date and end date of the current month
    start_date = date(current_date.year, current_date.month, 1).strftime('%Y-%m-%d')
    last_day = calendar.monthrange(current_date.year, current_date.month)[1]
    end_date = date(current_date.year, current_date.month, last_day).strftime('%Y-%m-%d')

    inventories = Inventory.objects.filter(date__range=[start_date, end_date])

    context = {
        'inventories': inventories,
        'products': products,
        'vehicles': vehicles,
        'drivers': drivers,
        'suppliers': suppliers,
        'customers': customers,
        'destinations': destinations,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'inventory.html', context)
# new added fields
# customer_ticket_no, factory_nett, bucket
# factory_nett = weight_in - weight_out
# bucket = deduction / 20
@login_required(login_url='login')
def add_inventory(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        ticket_no = data.get('ticket_no')
        date = data.get('date')
        customer_ticket_no = data.get('customer_ticket_no')
        vehicle = data.get('vehicle')
        driver = data.get('driver')
        supplier = data.get('supplier')

        supplier_qty = data.get('supplier_qty')
        customer = data.get('customer')
        product = data.get('product')
        _do = data.get('_do')
        weight_in = data.get('weight_in')
        weight_out = data.get('weight_out')
        factory_nett = data.get('factory_nett')
        deduction = data.get('deduction')
        bucket = data.get('bucket')
        remarks = data.get('remarks')

        vehicle_id = Vehicle.objects.get(reg_no=vehicle)
        driver_id = Person.objects.get(code=driver)
        supplier_id = Person.objects.get(code=supplier)
        customer_id = Person.objects.get(code=customer)
        product_id = Product.objects.get(code=product) 
        
        # Check if the inventory is in database
        inventory = Inventory.objects.filter(ticket_no=ticket_no, do=_do).first()
        
        if inventory is not None:
            return JsonResponse({'message': 'Inventory already exists!'}, status=400)
        else:
            # Add inventory to database
            inventory = Inventory(ticket_no=ticket_no, 
                                  date=date, 
                                  vehicle=vehicle_id, 
                                  driver=driver_id, 
                                  supplier=supplier_id, 
                                  supplier_qty=supplier_qty, 
                                  customer=customer_id,
                                  product=product_id, 
                                  do=_do, 
                                  weight_in=weight_in, 
                                  weight_out=weight_out, 
                                  deduction=deduction, 
                                  remark=remarks,
                                  customer_ticket_no=customer_ticket_no,
                                  factory_nett=factory_nett,
                                  bucket=bucket)
            inventory.save()
            return JsonResponse({'message': 'Success', 'new_id': inventory.id}, status=200)
    return JsonResponse({'message': 'Method not allowed'}, status=400)

@login_required(login_url='login')
def delete_inventory(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id = data.get('id')
        inventory = Inventory.objects.get(id=id)
        inventory.delete()
        return JsonResponse({'message': 'Success'}, status=200)
    return JsonResponse({'message': 'Method not allowed'}, status=400)

@login_required(login_url='login')
def edit_inventory(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id = data.get('id')
        ticket_no = data.get('ticket_no')
        date = data.get('date')
        
        vehicle = data.get('vehicle')
        driver = data.get('driver')
        supplier = data.get('supplier')
        customer_ticket_no = data.get('customer_ticket_no')
        supplier_qty = data.get('supplier_qty')
        customer = data.get('customer')
        product = data.get('product')
        _do = data.get('do')
        weight_in = data.get('weight_in')
        weight_out = data.get('weight_out')
        factory_nett = data.get('factory_nett')
        deduction = data.get('deduction')
        bucket = data.get('bucket')
        remarks = data.get('remarks')

        vehicle_id = Vehicle.objects.get(reg_no=vehicle)
        driver_id = Person.objects.get(code=driver)
        supplier_id = Person.objects.get(code=supplier)
        customer_id = Person.objects.get(code=customer)
        product_id = Product.objects.get(code=product) 

        print('supplier_qty : '+supplier_qty)
        
        try:
            # Try to get the inventory by id
            inventory = Inventory.objects.get(id=id)
            # Update the existing inventory
            inventory.ticket_no = ticket_no
            inventory.date = date
            inventory.vehicle = vehicle_id
            inventory.driver = driver_id
            inventory.supplier = supplier_id
            inventory.supplier_qty = supplier_qty
            inventory.customer = customer_id
            inventory.product = product_id
            inventory.do = _do
            inventory.weight_in = weight_in
            inventory.weight_out = weight_out
            inventory.deduction = deduction
            inventory.remark = remarks
            inventory.customer_ticket_no = customer_ticket_no
            inventory.factory_nett = factory_nett
            inventory.bucket = bucket
            inventory.save()
            return JsonResponse({'message': 'Success', 'new_id': inventory.id}, status=200)
        except Inventory.DoesNotExist:
            return JsonResponse({'message': 'Inventory not found'}, status=404)

    return JsonResponse({'message': 'Method not allowed'}, status=400)

