from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Destination
import json
# Create your views here.

@login_required(login_url='login')
def destinations(request):
    destinations = Destination.objects.all()
    context = {
        'destinations': destinations,
    }
    return render(request, 'destinations.html', context)


@login_required(login_url='login')
def add_dest(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        code = data.get('code')
        name = data.get('name')

        # Check if the destination is in database
        destination = Destination.objects.filter(code=code).first()
        
        if destination is not None:
            return JsonResponse({'message': 'Destination already exists!'}, status=400)
        else:
            # Add destination to database
            destination = Destination(code=code, name=name)
            destination.save()
            return JsonResponse({'message': 'Success', 'new_id': destination.id}, status=200)
    return JsonResponse({'message': 'Method not allowed'}, status=400)

@login_required(login_url='login')
def delete_dest(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id = data.get('id')

        # Check if the destination is in database
        destination = Destination.objects.filter(id=id).first()
        
        if destination is not None:
            destination.delete()
            return JsonResponse({'message': 'Success'}, status=200)
        else:
            return JsonResponse({'message': 'Destination does not exist!'}, status=400)
    return JsonResponse({'message': 'Method not allowed'}, status=400)

@login_required(login_url='login')
def edit_dest(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id = data.get('id')
        code = data.get('code')
        name = data.get('name')

        # Check if the destination is in database
        destination = Destination.objects.filter(id=id).first()
        
        if destination is not None:
            destination.code = code
            destination.name = name
            destination.save()
            return JsonResponse({'message': 'Success'}, status=200)
        else:
            return JsonResponse({'message': 'Destination does not exist!'}, status=400)
    return JsonResponse({'message': 'Method not allowed'}, status=400)