from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Vehicle
import json

# Create your views here.
@login_required(login_url='login')
def vehicles(request):
    vehicles = Vehicle.objects.all()
    context = {
        'vehicles': vehicles,
    }
    return render(request, 'vehicle.html', context)

@login_required(login_url='login')
def add_vehicle(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        reg_no = data.get('reg_no')
        model = data.get('model')

        # Check if the vehicle is in database
        vehicle = Vehicle.objects.filter(reg_no=reg_no, model=model).first()
        
        if vehicle is not None:
            return JsonResponse({'message': 'Vehicle already exists!'}, status=400)
        else:
            # Add vehicle to database
            vehicle = Vehicle(reg_no=reg_no, model=model)
            vehicle.save()
            return JsonResponse({'message': 'Success', 'new_id': vehicle.id}, status=200)
    return JsonResponse({'message': 'Method not allowed'}, status=400)

@login_required(login_url='login')
def delete_vehicle(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id = data.get('id')

        # Check if the vehicle is in database
        vehicle = Vehicle.objects.filter(id=id).first()
        
        if vehicle is not None:
            vehicle.delete()
            return JsonResponse({'message': 'Success'}, status=200)
        else:
            return JsonResponse({'message': 'Vehicle does not exist!'}, status=400)
    return JsonResponse({'message': 'Method not allowed'}, status=400)

@login_required(login_url='login')
def edit_vehicle(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id = data.get('id')
        reg_no = data.get('reg_no')
        model = data.get('model')

        # Check if the vehicle is in database
        vehicle = Vehicle.objects.filter(id=id).first()
        
        if vehicle is not None:
            vehicle.reg_no = reg_no
            vehicle.model = model
            vehicle.save()
            return JsonResponse({'message': 'Success'}, status=200)
        else:
            return JsonResponse({'message': 'Vehicle does not exist!'}, status=400)
    return JsonResponse({'message': 'Method not allowed'}, status=400)