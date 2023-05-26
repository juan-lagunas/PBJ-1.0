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
            method = 'Add',
            quantity = quantity,
            user = request.user.username,
            date = date,
        )

        return render(request, 'inventory/index.html', {
            'success': f'Successfully updated inventory for {part_data.name}'
        })


    # Edit inventory
    if request.method == 'POST' and 'edit_form' in request.POST:
        part = request.POST['part'].title()
        update_name = request.POST['update_name'].title()
        update_category = request.POST['update_category'].title()
        update_quantity = request.POST['update_quantity']
        update_price = request.POST['update_price']

        if not part:
            return render(request, 'inventory/index.html', {
                'fail': 'Must provide a part name.'
            })
        
        # Check that part exists in inventory
        try:
            part_data = Part.objects.get(name=part)
            inventory_data = Inventory.objects.get(part=part_data)
            # Get old data to display changes made
            old_inventory = Inventory.objects.get(part=part_data)
            old_category = part_data.category
            old_price = part_data.usd
            old_total = old_inventory.total
        except:
            return render(request, 'inventory/index.html', {
                'fail': 'Part not found in inventory.'
            })
        

        # Get category data if exist else create new category
        try:
            category_data = Category.objects.get(category=update_category)
        except:
            category_data = Category.objects.create(category=update_category)
        
        
        # Change values of part if information was provided
        if update_name:
            part_data.name = update_name

        if update_category:
            part_data.category = category_data
        
        if update_price:
            try:
                update_price = float(update_price)
            except ValueError:
                return render(request, 'inventory/index.html', {
                    'fail': 'Price not a valid value.'
                })
            part_data.price = update_price

        if update_quantity:
            try:
                update_quantity = int(update_quantity)
            except ValueError:
                return render(request, 'inventory/index.html', {
                    'fail': 'Quantity not a valid value.'
                })
            inventory_data.quantity = update_quantity


        # Save after all changes have been made
        part_data.save()
        inventory_data.save()

        # Get data about the updated part inorder to log info about the change else use provided part
        if update_name:
            part_to_log = Part.objects.get(name=update_name)
        else:
            part_to_log = Part.objects.get(name=part)

        part_inventory = Inventory.objects.get(part=part_to_log)

        date = datetime.datetime.now()
        Log.objects.create(
            part = part_to_log,
            method = 'Edit',
            quantity = part_inventory.quantity,
            user = request.user.username,
            date = date,
        )

        return render(request, 'inventory/index.html', {
            'success': f'Succesfully changed  to {part_inventory}',
            'previous': f'from ({old_category}) {part} Qty: {old_inventory.quantity} Price: {old_price} Total: {old_total}'
        })



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


@login_required
def logs(request):
    date = datetime.date.today()
    today = Log.objects.filter(date__contains=date).order_by('-date')
    yesterday = Log.objects.filter(date__contains=date-datetime.timedelta(days=1)).order_by('-date')
    return render(request, 'inventory/logs.html', {
        'today': today,
        'yesterday': yesterday,
    })
    

@login_required
def browse(request):
    inventory = Inventory.objects.all()
    categories = set()
    for part in inventory:
        categories.add(part.part.category)

    return render(request, 'inventory/browse.html', {
        'inventory': inventory,
        'categories': categories
    })