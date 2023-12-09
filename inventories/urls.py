from django.urls import path
from . import views

urlpatterns = [
    path('', views.inventories, name='inventories'),
    path('add_inventory/', views.add_inventory, name='add_inventory'),
    path('edit_inventory/', views.edit_inventory, name='edit_inventory'),
    path('delete_inventory/', views.delete_inventory, name='delete_inventory'),
]