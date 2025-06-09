from django.db import models
from django.contrib.auth.models import User

class Trip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    destination = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    purpose = models.CharField(max_length=50, choices=[
        ('mountains', 'Góry'),
        ('beach', 'Plaża'),
        ('city', 'Miasto'),
        ('camping', 'Camping'),
    ])
    weather_info = models.TextField(blank=True)

class Item(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=50, choices=[
        ('handbag', 'Torba podręczna'),
        ('suitcase', 'Walizka'),
        ('backpack', 'Plecak'),
    ])
    weight = models.FloatField(default=0.0)
    is_packed = models.BooleanField(default=False)

class Reminder(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    task = models.CharField(max_length=200)
    due_date = models.DateField(null=True, blank=True)
    is_done = models.BooleanField(default=False)

class Alert(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    message = models.CharField(max_length=200)
    date = models.DateField()
    is_active = models.BooleanField(default=True)