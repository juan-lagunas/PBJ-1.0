from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import datetime
# Create your views here.

def index(request):
    return render(request, 'core/index.html')

def signin(request):
    return render(request, 'core/login.html')

def signup(request):
    return render(request, 'core/signup.html')