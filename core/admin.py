from django.contrib import admin
from .models import TravelGroup, Trip, Category, Item, ShoppingItem, Reminder, Alert, PackingList, PackingItem, PreTripTask

@admin.register(TravelGroup)
class TravelGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    filter_horizontal = ('members',)
    search_fields = ('name', 'members__username')

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ['destination', 'owner', 'start_date', 'end_date']
    list_filter = ['start_date', 'end_date']
    search_fields = ['destination', 'owner__username']
    date_hierarchy = 'start_date'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')
    search_fields = ('name',)

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'trip', 'category', 'location', 'weight', 'is_packed', 'is_essential')
    list_filter = ('location', 'is_packed', 'is_essential', 'category')
    search_fields = ('name', 'trip__destination', 'category__name')

@admin.register(PackingList)
class PackingListAdmin(admin.ModelAdmin):
    list_display = ['name', 'trip', 'estimated_weight', 'is_shared']
    list_filter = ['is_shared', 'trip__destination']
    search_fields = ['name', 'trip__destination']

@admin.register(PackingItem)
class PackingItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'packing_list', 'category', 'quantity', 'is_packed', 'location']
    list_filter = ['category', 'is_packed', 'location']
    search_fields = ['name', 'packing_list__name']

@admin.register(PreTripTask)
class PreTripTaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'trip', 'due_date', 'priority', 'is_completed']
    list_filter = ['priority', 'is_completed', 'due_date']
    search_fields = ['title', 'description']
    date_hierarchy = 'due_date'

@admin.register(ShoppingItem)
class ShoppingItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'trip', 'estimated_price', 'is_purchased']
    list_filter = ['is_purchased']
    search_fields = ['name', 'trip__destination']

@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ('task', 'trip', 'due_date', 'priority', 'is_done')
    list_filter = ('priority', 'is_done', 'due_date')
    search_fields = ('task', 'trip__destination')
    date_hierarchy = 'due_date'

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ['title', 'trip', 'type', 'start_date', 'end_date', 'is_active']
    list_filter = ['type', 'is_active', 'start_date']
    search_fields = ['title', 'message', 'trip__destination']
    date_hierarchy = 'start_date'
