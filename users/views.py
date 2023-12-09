from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

# Create your views here.
@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Check if user is in database
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, ('You have been logged in!'))
            # redirect to home page
            return redirect('home')
        else:
            messages.success(request, ('Error logging in - Please try again...'))
            return render(request, 'authenticate/login.html', {})   
    else:
        return render(request, 'authenticate/login.html', {})
    
def logout_user(request):
    logout(request)
    messages.success(request, ('You have been logged out!'))
    # redirect to login page
    return render(request, 'authenticate/login.html', {})

@login_required(login_url='login')
def home(request):
    return render(request, 'home.html', {})
