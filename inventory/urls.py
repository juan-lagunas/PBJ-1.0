from django.urls import path

from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.index, name='index'),
    path('logs/', views.logs, name='logs'),
    path('browse/', views.browse, name='browse'),
]