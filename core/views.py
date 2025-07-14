from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.utils import timezone
from .models import Trip, Item, Reminder, Alert, PreTripTask
from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .forms import TripForm

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, _('Nieprawidłowa nazwa użytkownika lub hasło.'))
    
    return render(request, 'registration/login.html')

@login_required
def dashboard(request):
    active_trips = Trip.objects.filter(
        owner=request.user,
        end_date__gte=timezone.now()
    ).order_by('start_date')

    tasks = PreTripTask.objects.filter(
        trip__owner=request.user,
        is_completed=False
    ).order_by('due_date')[:3]

    alerts = Alert.objects.filter(
        trip__owner=request.user,
        is_active=True
    ).order_by('-created_at')[:2]

    context = {
        'active_trips': active_trips,
        'tasks': tasks,
        'alerts': alerts,
    }
    
    return render(request, 'core/dashboard.html', context)

@login_required
def add_trip(request):
    if request.method == 'POST':
        form = TripForm(request.POST)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.owner = request.user
            trip.save()
            messages.success(request, _('Podróż została dodana pomyślnie!'))
            return redirect('dashboard')
    else:
        form = TripForm()
    
    return render(request, 'core/add_trip.html', {'form': form})

@login_required
def trip_details(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id, owner=request.user)
    return render(request, 'core/trip_details.html', {'trip': trip})

@login_required
def delete_trip(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id, owner=request.user)
    if request.method == 'POST':
        trip.delete()
        messages.success(request, _('Podróż została usunięta pomyślnie!'))
        return redirect('dashboard')
    return redirect('trip_details', trip_id=trip_id)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def custom_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'registration/login.html', {'hide_navbar': True})