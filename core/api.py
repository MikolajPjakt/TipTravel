from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django.utils import timezone
import requests
from datetime import timedelta

from .models import TravelGroup, Trip, Category, Item, ShoppingItem, Reminder, Alert
from .serializers import (
    TravelGroupSerializer, TripSerializer, CategorySerializer,
    ItemSerializer, ShoppingItemSerializer, ReminderSerializer,
    AlertSerializer, UserSerializer
)
from django.conf import settings

class TravelGroupViewSet(viewsets.ModelViewSet):
    serializer_class = TravelGroupSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TravelGroup.objects.filter(members=self.request.user)

    def perform_create(self, serializer):
        group = serializer.save()
        group.members.add(self.request.user)

class TripViewSet(viewsets.ModelViewSet):
    serializer_class = TripSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Trip.objects.filter(
            models.Q(user=self.request.user) |
            models.Q(group__members=self.request.user)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['get'])
    def fetch_weather(self, request, pk=None):
        trip = self.get_object()
        api_key = settings.OPENWEATHERMAP_API_KEY
        
        if not api_key:
            return Response(
                {"error": "OpenWeatherMap API key not configured"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        # Get weather forecast for the trip dates
        base_url = "http://api.openweathermap.org/data/2.5/forecast"
        params = {
            "q": trip.destination,
            "appid": api_key,
            "units": "metric",
            "lang": "pl"
        }

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            weather_data = response.json()
            
            # Update trip's weather info
            trip.weather_info = weather_data
            trip.save()
            
            return Response(weather_data)
        except requests.exceptions.RequestException as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        trip = self.get_object()
        total_weight = trip.items.aggregate(Sum('weight'))['weight__sum'] or 0
        packed_items = trip.items.filter(is_packed=True).count()
        total_items = trip.items.count()
        essential_items = trip.items.filter(is_essential=True).count()
        
        return Response({
            "total_weight": total_weight,
            "packed_items": packed_items,
            "total_items": total_items,
            "packing_progress": (packed_items / total_items * 100) if total_items > 0 else 0,
            "essential_items": essential_items,
            "days_until_trip": (trip.start_date - timezone.now().date()).days if trip.start_date > timezone.now().date() else 0,
        })

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Item.objects.filter(
            models.Q(trip__user=self.request.user) |
            models.Q(trip__group__members=self.request.user)
        ).distinct()

    def perform_update(self, serializer):
        if 'is_packed' in self.request.data and self.request.data['is_packed']:
            serializer.save(packed_by=self.request.user)
        else:
            serializer.save()

class ShoppingItemViewSet(viewsets.ModelViewSet):
    serializer_class = ShoppingItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ShoppingItem.objects.filter(
            models.Q(trip__user=self.request.user) |
            models.Q(trip__group__members=self.request.user)
        ).distinct()

class ReminderViewSet(viewsets.ModelViewSet):
    serializer_class = ReminderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Reminder.objects.filter(
            models.Q(trip__user=self.request.user) |
            models.Q(trip__group__members=self.request.user)
        ).distinct()

    def perform_update(self, serializer):
        if 'is_done' in self.request.data and self.request.data['is_done']:
            serializer.save(
                completed_by=self.request.user,
                completed_at=timezone.now()
            )
        else:
            serializer.save()

class AlertViewSet(viewsets.ModelViewSet):
    serializer_class = AlertSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Alert.objects.filter(
            models.Q(trip__user=self.request.user) |
            models.Q(trip__group__members=self.request.user)
        ).distinct()

    @action(detail=False, methods=['get'])
    def active(self, request):
        alerts = self.get_queryset().filter(
            is_active=True,
            date__gte=timezone.now() - timedelta(days=7)
        )
        serializer = self.get_serializer(alerts, many=True)
        return Response(serializer.data) 