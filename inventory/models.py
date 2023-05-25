from django.db import models

# Create your models here.

class Category(models.Model):
    category =  models.CharField(max_length=64)

    def __str__(self):
        return self.category
    

class Part(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=100)
    price = models.FloatField()
    date = models.DateField()

    @property
    def usd(self):
        return f'${self.price:,.2f}'

    def __str__(self):
        return f'({self.category}) {self.name} {self.usd}'
    

class Inventory(models.Model):
    part = models.ForeignKey(Part, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()

    @property
    def total(self):
        value = self.part.price * self.quantity
        return f'${value:,.2f}'
    
    def __str__(self):
        return f'({self.part.category}) {self.part.name} Qty: {self.quantity} Price: {self.part.usd} Total: {self.total}'
    

class Log(models.Model):
    part = models.ForeignKey(Part, on_delete=models.SET_NULL, null=True)
    method = models.CharField(max_length=40)
    quantity = models.IntegerField()
    user = models.CharField(max_length=40)
    date = models.DateTimeField()

    @property
    def total(self):
        value = self.part.price * self.quantity
        return f'${value:,.2f}'
    
    def __str__(self):
        return f'({self.part.category}) {self.part.name} {self.method} Qty: {self.quantity} Total: {self.total} User: {self.user} Date: {self.date}'