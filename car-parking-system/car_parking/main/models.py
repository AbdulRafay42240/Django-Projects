from django.db import models

# Create your models here.
class addvehicle(models.Model):
    car_name = models.CharField(max_length=100)
    car_plate = models.CharField(max_length=6)
    driver_name = models.CharField(max_length=100)
    driver_contact = models.IntegerField(default=0)
    parking_time = models.CharField(max_length=100)
