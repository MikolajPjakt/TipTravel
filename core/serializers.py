from rest_framework import serializers
from django.contrib.auth.models import User
from .models import TravelGroup, Trip, Category, Item, ShoppingItem, Reminder, Alert

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class TravelGroupSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)
    member_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        write_only=True,
        source='members'
    )

    class Meta:
        model = TravelGroup
        fields = ['id', 'name', 'members', 'member_ids', 'created_at']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'icon']

class ItemSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    packed_by_name = serializers.CharField(source='packed_by.username', read_only=True)

    class Meta:
        model = Item
        fields = [
            'id', 'trip', 'category', 'category_name', 'name', 'quantity',
            'location', 'weight', 'is_packed', 'is_essential', 'notes',
            'packed_by', 'packed_by_name', 'created_at', 'updated_at'
        ]

class ShoppingItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingItem
        fields = [
            'id', 'trip', 'name', 'estimated_price', 'is_purchased',
            'priority', 'notes', 'created_at', 'updated_at'
        ]

class ReminderSerializer(serializers.ModelSerializer):
    completed_by_name = serializers.CharField(source='completed_by.username', read_only=True)

    class Meta:
        model = Reminder
        fields = [
            'id', 'trip', 'task', 'description', 'due_date', 'priority',
            'is_done', 'completed_by', 'completed_by_name', 'completed_at',
            'created_at', 'updated_at'
        ]

class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = [
            'id', 'trip', 'type', 'title', 'message', 'source_url',
            'date', 'is_active', 'created_at', 'updated_at'
        ]

class TripSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)
    shopping_items = ShoppingItemSerializer(many=True, read_only=True)
    reminders = ReminderSerializer(many=True, read_only=True)
    alerts = AlertSerializer(many=True, read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    group_name = serializers.CharField(source='group.name', read_only=True)

    class Meta:
        model = Trip
        fields = [
            'id', 'user', 'user_name', 'group', 'group_name', 'destination',
            'start_date', 'end_date', 'purpose', 'weather_info', 'notes',
            'items', 'shopping_items', 'reminders', 'alerts',
            'created_at', 'updated_at'
        ] 