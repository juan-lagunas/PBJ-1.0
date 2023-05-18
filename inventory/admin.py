from django.contrib import admin

from .models import Category, Part, Inventory, Log

class AdminCategory(admin.ModelAdmin):
    list_display = ('id', 'category')

class AdminPart(admin.ModelAdmin):
    list_display = ('id', 'category', 'name', 'description', 'price', 'date')


class AdminInventory(admin.ModelAdmin):
    list_display = ('id', 'part', 'quantity', 'total')
    
class AdminLog(admin.ModelAdmin):
    list_display = ('id', 'part', 'quantity', 'total', 'user', 'date')

admin.site.register(Inventory, AdminInventory)
admin.site.register(Log, AdminLog)

admin.site.register(Category, AdminCategory)
admin.site.register(Part, AdminPart)