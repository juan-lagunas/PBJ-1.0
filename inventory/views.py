from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Part, Category, Inventory, Log
import datetime

# Create your views here.

@login_required
def index(request):

    # Add inventory
    if request.method == 'POST' and 'add_form' in request.POST:
        part = request.POST['part'].title()\
        
        # Check that quantity is valid float number
        try:
            quantity = int(request.POST['quantity'])
        except ValueError:
            return render(request, 'inventory/index.html', {
                'fail': 'Quantity not of correct value.'
            })
        
        # Check that user filled out everything
        if not part or not quantity:
            return render(request, 'inventory/index.html', {
                'fail': 'Need to fill out both part and quanitity.'
            })
        
        # Check if part exists
        try:
            part_data = Part.objects.get(name=part)
        except:
            return render(request, 'inventory/index.html', {
                'fail': 'Part not found'
            })
        
        # Check if part already in inventory to update quantity if not create it
        try:
            inventory = Inventory.objects.get(part=part_data)
            inventory.quantity += quantity
            inventory.save()
        except:
            Inventory.objects.create(
                part=part_data,
                quantity = quantity,
            )
        
        # Create log for update of inventory
        date = datetime.datetime.now()
        Log.objects.create(
            part = part_data,
            quantity = quantity,
            user = request.user.username,
            date = date,
        )

        return render(request, 'inventory/index.html', {
            'success': f'Successfully updated inventory for {part_data.name}'
        })


    # Edit inventory
    if request.method == 'POST' and 'edit_form' in request.POST:
        passs


    # Create inventory
    if request.method == 'POST' and 'create_form' in request.POST:
        part = request.POST['part'].title()
        category = request.POST['category'].title()
        description = request.POST['description'].title()
        price = request.POST['price']
        if not part or not category or not description or not price:
            return render(request, 'inventory/index.html', {
                'fail': 'Need to fill out everything.'
            })

        try:
            price = float(price)
        except ValueError:
            return render(request, 'inventory/index.html', {
                'fail': 'price not of correct value.'
            })

        date = datetime.date.today()

        if Part.objects.filter(name=part).exists():
            return render(request, 'inventory/index.html', {
                'fail': 'Part with name already exists.'
            })
        

        category_data = Category.objects.filter(category=category)
        if category_data.exists():
            Part.objects.create(
                name = part,
                category = category_data.first(),
                description = description,
                price = price,
                date = date,
            )
        else:
            category_data = Category.objects.create(category=category)
            Part.objects.create(
                name = part,
                category = category_data,
                description = description,
                price = price,
                date = date,
            )

        return render(request, 'inventory/index.html', {
            'success': 'Sucessfully created part.'
        })
        
        
    return render(request, 'inventory/index.html')

