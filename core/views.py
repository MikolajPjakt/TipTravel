from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Trip, Item, Reminder, Alert

@login_required  # Requires user to be logged in
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if not authenticated
    trips = Trip.objects.filter(user=request.user)
    items = Item.objects.filter(trip__in=trips)
    reminders = Reminder.objects.filter(trip__in=trips)
    alerts = Alert.objects.filter(trip__in=trips, is_active=True)
    return render(request, 'core/dashboard.html', {
        'trips': trips,
        'items': items,
        'reminders': reminders,
        'alerts': alerts,
    })