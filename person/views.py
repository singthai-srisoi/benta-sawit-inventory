from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from .models import Person
import json
# Create your views here.

from django.views import View
from django.db import transaction
from django.forms.models import model_to_dict

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


def new_person_view(request):
    return render(request, 'new_person.html')

class PersonView(View):
    def get(self, request):
        data = request.GET
        type = data.get('type', None)

        page = int(data.get('page', 1))
        limit = int(data.get('limit', 10))
        start = (page - 1) * limit
        end = start + limit        

        search = data.get('search', 'false')

        if type is None:
            return JsonResponse({'message': 'Invalid data!'}, status=400)
        
        total_page = Person.objects.filter(type=type).count() // limit + 1
        if page > total_page:
            return JsonResponse({'message': 'Page not found!'}, status=404)
        
        if search == 'true':
            search_data = {
                'name__contains': data.get('name', ''),
                'code__contains': data.get('code', ''),
                'phone__contains': data.get('phone', ''),
                'ic__contains': data.get('ic', ''),
            }

            persons = Person.objects.filter(type=type, **search_data)[start:end]
            persons = persons.as_dict()
            data = {'data': persons, 'total_page': total_page, 'page': page, 'limit': limit,}
            return JsonResponse(data, status=200)
        else:
            persons = Person.objects.filter(type=type)[start:end]
            persons = persons.as_dict()
            data = {'data': persons, 'total_page': total_page, 'page': page, 'limit': limit,}
            return JsonResponse(data, status=200, safe=False)
    
    def post(self, request):
        with transaction.atomic():
            data: dict = json.loads(request.body)

            if data.get('code', None) == None or data.get('type', None) == None:
                return JsonResponse({'message': 'Invalid data!'}, status=400)

            person = Person.objects.filter(code=data.get('code'), type=data.get('type')).first()
            
            if person:
                return JsonResponse({'message': 'Person already exists!'}, status=400)
            else:
                person = Person(**data)
                person.save()
                data['id'] = person.id
                return JsonResponse(data, status=200)
            
    def put(self, request):
        with transaction.atomic():
            data: dict = json.loads(request.body)

            if data.get('id', None) == None:
                return JsonResponse({'message': 'Invalid data!'}, status=400)

            person = Person.objects.filter(id=data.get('id')).first()
            if person:
                for key, value in data.items():
                    setattr(person, key, value)
                person.save()
                return JsonResponse(data, status=200)
            else:
                return JsonResponse({'message': 'Person does not exist!'}, status=400)
            
    def delete(self, request):
        with transaction.atomic():
            data: dict = json.loads(request.body)

            if data.get('id', None) == None:
                return JsonResponse({'message': 'Invalid data!'}, status=400)

            person = Person.objects.filter(id=data.get('id')).first()
            if person:
                person.delete()
                return JsonResponse({'message': 'Success'}, status=200)
            else:
                return JsonResponse({'message': 'Person does not exist!'}, status=400)
        
