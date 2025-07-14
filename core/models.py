from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class TravelGroup(models.Model):
    name = models.CharField(_('Nazwa grupy'), max_length=100)
    members = models.ManyToManyField(User, related_name='travel_groups')
    created_at = models.DateTimeField(_('Data utworzenia'), default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Grupa podróżna')
        verbose_name_plural = _('Grupy podróżne')

class Trip(models.Model):
    TRIP_PURPOSES = [
        ('mountains', _('Góry')),
        ('beach', _('Plaża')),
        ('city', _('Miasto')),
        ('camping', _('Camping')),
        ('business', _('Służbowy')),
        ('other', _('Inny')),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_trips')
    participants = models.ManyToManyField(User, related_name='participated_trips', blank=True)
    group = models.ForeignKey(TravelGroup, on_delete=models.SET_NULL, null=True, blank=True, related_name='trips')
    destination = models.CharField(_('Cel podróży'), max_length=100)
    start_date = models.DateField(_('Data rozpoczęcia'))
    end_date = models.DateField(_('Data zakończenia'))
    purpose = models.CharField(_('Cel'), max_length=50, choices=TRIP_PURPOSES)
    weather_info = models.JSONField(_('Informacje o pogodzie'), default=dict, blank=True)
    notes = models.TextField(_('Notatki'), blank=True)
    created_at = models.DateTimeField(_('Data utworzenia'), default=timezone.now)
    updated_at = models.DateTimeField(_('Data aktualizacji'), auto_now=True)

    def __str__(self):
        return f"{self.destination} ({self.start_date} - {self.end_date})"

    class Meta:
        verbose_name = _('Podróż')
        verbose_name_plural = _('Podróże')
        ordering = ['-start_date']

class Category(models.Model):
    name = models.CharField(_('Nazwa'), max_length=50)
    icon = models.CharField(_('Ikona'), max_length=50, blank=True)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Kategoria')
        verbose_name_plural = _('Kategorie')

class Item(models.Model):
    LOCATIONS = [
        ('handbag', _('Torba podręczna')),
        ('suitcase', _('Walizka')),
        ('backpack', _('Plecak')),
        ('other', _('Inne')),
    ]

    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='items')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='items')
    name = models.CharField(_('Nazwa'), max_length=100)
    quantity = models.PositiveIntegerField(_('Ilość'), default=1)
    location = models.CharField(_('Lokalizacja'), max_length=50, choices=LOCATIONS)
    weight = models.FloatField(_('Waga (kg)'), default=0.0)
    is_packed = models.BooleanField(_('Spakowane'), default=False)
    is_essential = models.BooleanField(_('Niezbędne'), default=False)
    notes = models.TextField(_('Notatki'), blank=True)
    packed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='packed_items')
    created_at = models.DateTimeField(_('Data utworzenia'), default=timezone.now)
    updated_at = models.DateTimeField(_('Data aktualizacji'), auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.trip.destination})"

    class Meta:
        verbose_name = _('Przedmiot')
        verbose_name_plural = _('Przedmioty')
        ordering = ['category', 'name']

class ShoppingItem(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='shopping_items')
    name = models.CharField(max_length=100)
    estimated_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_purchased = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Lista zakupów')
        verbose_name_plural = _('Lista zakupów')
        ordering = ['-created_at']

class Reminder(models.Model):
    PRIORITY_CHOICES = [
        (1, _('Niski')),
        (2, _('Średni')),
        (3, _('Wysoki')),
    ]

    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='reminders')
    task = models.CharField(_('Zadanie'), max_length=200)
    description = models.TextField(_('Opis'), blank=True)
    due_date = models.DateTimeField(_('Termin'), null=True, blank=True)
    priority = models.IntegerField(_('Priorytet'), choices=PRIORITY_CHOICES, default=2)
    is_done = models.BooleanField(_('Wykonane'), default=False)
    completed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='completed_reminders')
    completed_at = models.DateTimeField(_('Data wykonania'), null=True, blank=True)
    created_at = models.DateTimeField(_('Data utworzenia'), default=timezone.now)
    updated_at = models.DateTimeField(_('Data aktualizacji'), auto_now=True)

    def __str__(self):
        return f"{self.task} ({self.trip.destination})"

    class Meta:
        verbose_name = _('Przypomnienie')
        verbose_name_plural = _('Przypomnienia')
        ordering = ['-priority', 'due_date']

class Alert(models.Model):
    ALERT_TYPES = [
        ('weather', _('Pogoda')),
        ('security', _('Bezpieczeństwo')),
        ('transport', _('Transport')),
        ('other', _('Inne')),
    ]

    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='alerts')
    type = models.CharField(max_length=20, choices=ALERT_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.trip.destination}"

    class Meta:
        verbose_name = _('Alert')
        verbose_name_plural = _('Alerty')
        ordering = ['-created_at']

class PackingList(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='packing_lists')
    name = models.CharField(max_length=100)
    estimated_weight = models.FloatField(null=True, blank=True)
    is_shared = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.trip.destination}"

class PackingItem(models.Model):
    CATEGORY_CHOICES = [
        ('clothes', _('Ubrania')),
        ('electronics', _('Elektronika')),
        ('toiletries', _('Kosmetyki')),
        ('documents', _('Dokumenty')),
        ('other', _('Inne'))
    ]

    LOCATION_CHOICES = [
        ('main_luggage', _('Bagaż główny')),
        ('hand_luggage', _('Bagaż podręczny')),
        ('backpack', _('Plecak')),
        ('other', _('Inne'))
    ]

    packing_list = models.ForeignKey(PackingList, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    quantity = models.IntegerField(default=1)
    weight = models.FloatField(null=True, blank=True)  # in kg
    is_packed = models.BooleanField(default=False)
    location = models.CharField(max_length=20, choices=LOCATION_CHOICES, default='main_luggage')
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.quantity}x)"

class PreTripTask(models.Model):
    PRIORITY_CHOICES = [
        ('high', _('Wysoki')),
        ('medium', _('Średni')),
        ('low', _('Niski'))
    ]

    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['due_date', '-priority']

    def __str__(self):
        return self.title