from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Person
import json
# Create your views here.

@login_required(login_url='login')
def customer(request):
    customers = Person.objects.filter(type='customer')
    context = {
        'persons': customers,
        'type': 'customer',
    }
    return render(request, 'customer.html', context)

@login_required(login_url='login')
def supplier(request):
    suppliers = Person.objects.filter(type='supplier')
    context = {
        'persons': suppliers,
        'type': 'supplier',
    }
    return render(request, 'customer.html', context)

@login_required(login_url='login')
def driver(request):
    drivers = Person.objects.filter(type='driver')
    context = {
        'persons': drivers,
        'type': 'driver',
    }
    return render(request, 'customer.html', context)


@login_required(login_url='login')
def add_person(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        code = data.get('code')
        name = data.get('name')
        phone = data.get('phone')
        ic = data.get('ic')
        type = data.get('type')

        # Check if the person of that type is in database
        person = Person.objects.filter(code=code, type=type).first()
        
        if person is not None:
            return JsonResponse({'message': 'Person already exists!'}, status=400)
        else:
            # Add person to database
            person = Person(code=code, name=name, phone=phone, ic=ic, type=type)
            person.save()
            return JsonResponse({'message': 'Success', 'new_id': person.id}, status=200)
    return JsonResponse({'message': 'Method not allowed'}, status=400)

@login_required(login_url='login')
def delete_person(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id = data.get('id')

        # Check if person is in database
        person = Person.objects.filter(id=id).first()
        
        if person is None:
            return JsonResponse({'message': 'Person does not exist!'}, status=400)
        else:
            # Delete person from database
            person.delete()
            return JsonResponse({'message': 'Success'}, status=200)
    return JsonResponse({'message': 'Method not allowed'}, status=400)

@login_required(login_url='login')
def edit_person(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id = data.get('id')
        code = data.get('code')
        name = data.get('name')
        phone = data.get('phone')
        ic = data.get('ic')
        type = data.get('type')

        # Check if person is in database
        person = Person.objects.filter(id=id).first()
        
        if person is None:
            return JsonResponse({'message': 'Person does not exist!'}, status=400)
        else:
            # Edit person in database
            person.code = code
            person.name = name
            person.phone = phone
            person.ic = ic
            person.type = type
            person.save()

            return JsonResponse({'message': 'Success'}, status=200)
    return JsonResponse({'message': 'Method not allowed'}, status=400)