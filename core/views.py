from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    return render(request, 'core/index.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username'].title()
        password = request.POST['password']

        if not username or not password:
            return render(request, 'core/login.html', {
                'fail': 'Username or password not found.'
            })
        
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
            
        
        return render(request, 'core/login.html', {
                'fail': 'Username or password not found.'
            })
        
    return render(request, 'core/login.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username'].title()
        email = request.POST['email']
        password = request.POST['password']
        
        if not username or not email or not password:
            return render(request, 'core/signup.html', {
                'fail': 'Need to fill out everything.'
            })
        
        if User.objects.filter(username=username).exists():
            return render(request, 'core/signup.html', {
                'fail': 'Username already taken.'
            })
        
        user = User.objects.create_user(username, email, password)
        user.save()
        return render(request, 'core/login.html', {
                'success': 'Successfully signed up.'
            })


    return render(request, 'core/signup.html')


@login_required
def signout(request):
    logout(request)
    return redirect('/')