from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views, api

router = DefaultRouter()
router.register(r'groups', api.TravelGroupViewSet, basename='group')
router.register(r'trips', api.TripViewSet, basename='trip')
router.register(r'categories', api.CategoryViewSet, basename='category')
router.register(r'items', api.ItemViewSet, basename='item')
router.register(r'shopping', api.ShoppingItemViewSet, basename='shopping')
router.register(r'reminders', api.ReminderViewSet, basename='reminder')
router.register(r'alerts', api.AlertViewSet, basename='alert')

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add-trip/', views.add_trip, name='add_trip'),
    path('trip/<int:trip_id>/', views.trip_details, name='trip_details'),
    path('trip/<int:trip_id>/delete/', views.delete_trip, name='delete_trip'),
    path('login/', views.custom_login, name='login'),
    path('register/', views.register, name='register'),
]

