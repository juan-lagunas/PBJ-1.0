from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def index(request):
    return render(request, 'inventory/index.html')

@login_required
def edit(request):
    return render(request, 'inventory/edit.html')
