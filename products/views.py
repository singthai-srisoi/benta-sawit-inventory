from django.shortcuts import render, get_object_or_404
from .models import Product, ProductType
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import logging
import json

# Create your views here.
@login_required(login_url='login')
def products(request):
    products = Product.objects.all()
    product_types = ProductType.objects.all()
    context = {
        'products': products,
        'product_types': product_types,
    }
    return render(request, 'products.html', context)


@login_required(login_url='login')
def add_product(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        code = data.get('code')
        name = data.get('name')
        price = data.get('price')
        type_ = data.get('type')

        # if type is empty set type null
        if type_ == '':
            ptype = None
        else:
            ptype = ProductType.objects.get(code=type_)

        # Check if product is in database
        product = Product.objects.filter(code=code).first()
        
        if product is not None:
            return JsonResponse({'message': 'Product already exists!'}, status=400)
        else:
            # Add product to database
            product = Product(code=code, name=name, price=price, type=ptype)
            product.save()
            return JsonResponse({'message': 'Success', 'new_id': product.id}, status=200)
    return JsonResponse({'message': 'Method not allowed'}, status=400)

@login_required(login_url='login')
def edit_product(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id = data.get('id')
        code = data.get('code')
        name = data.get('name')
        price = data.get('price')
        type_ = data.get('type')


        # if type is empty set type null
        if type_ == '':
            ptype = None
        else:
            ptype = ProductType.objects.get(code=type_)

        print(code, name, price, type_)
        
        # Check if product is in database
        product = Product.objects.get(id=id)
        
        if product is not None:
            product.code = code
            product.name = name
            product.price = price
            if type is not None:
                product.type = ptype
            product.save()
            return JsonResponse({'message': 'Success'}, status=200)
        else:
            return JsonResponse({'message': 'Product does not exists!'}, status=400)
    return JsonResponse({'message': 'Method not allowed'}, status=400)

@login_required(login_url='login')
def delete_product(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id = data.get('id')

        print(id)
        
        # Check if product is in database
        product = Product.objects.get(id=id)
        
        if product is not None:
            Product.objects.filter(id=id).delete()
            #product.save()
            return JsonResponse({'message': 'Success'}, status=200)
        else:
            return JsonResponse({'message': 'Product does not exists!'}, status=400)
    return JsonResponse({'message': 'Method not allowed'}, status=400)

@login_required(login_url='login')
def product_types(request):
    #products = Product.objects.all()
    product_types = ProductType.objects.all()
    context = {
        #'products': products,
        'product_types': product_types,
    }
    return render(request, 'product_types.html', context)

@login_required(login_url='login')
def add_type(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        code = data.get('code')
        name = data.get('name')
        
        # Check if product is in database
        product = ProductType.objects.filter(code=code)
        
        if product.exists():
            return JsonResponse({'message': 'Product already exists!'}, status=400)
        else:
            # Add product to database
            product_type = ProductType(code=code, name=name)
            product_type.save()
            return JsonResponse({'message': 'Success'}, status=200)
    return JsonResponse({'message': 'Method not allowed'}, status=400)

@login_required(login_url='login')
def edit_type(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        code = data.get('code')
        name = data.get('name')

        print(code, name)
        
        # Check if product is in database
        product_type = ProductType.objects.get(code=code)
        
        if product_type is not None:
            product_type.name = name
            product_type.save()
            return JsonResponse({'message': 'Success'}, status=200)
        else:
            return JsonResponse({'message': 'Product does not exists!'}, status=400)
    return JsonResponse({'message': 'Method not allowed'}, status=400)

@login_required(login_url='login')
def delete_type(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        code = data.get('code')

        print(id)
        
        # Check if product is in database
        product_type = ProductType.objects.get(code=code)
        
        if product_type is not None:
            product_type.delete()
            #product.save()
            return JsonResponse({'message': 'Success'}, status=200)
        else:
            return JsonResponse({'message': 'Product does not exists!'}, status=400)
    return JsonResponse({'message': 'Method not allowed'}, status=400)