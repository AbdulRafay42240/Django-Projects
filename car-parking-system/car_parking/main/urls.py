from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path('',views.home, name='home'),
    path('add.html/',views.add, name='add'),
    path('remove.html/',views.remove, name='remove'),
    path('bill.html/',views.bill, name='bill'),
    path('view.html/',views.view, name='view'),
    path('recipt.html/',views.recipt, name='recipt')
]
