from django.urls import path
from . import views

urlpatterns = [
    path('', views.vehicles, name='vehicles'),
    path('add_vehicle/', views.add_vehicle, name='add_vehicle'),
    path('edit_vehicle/', views.edit_vehicle, name='edit_vehicle'),
    path('delete_vehicle/', views.delete_vehicle, name='delete_vehicle'),
]