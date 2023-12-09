from django.urls import path
from . import views

urlpatterns = [
    path('', views.destinations, name='destinations'),
    path('add_dest', views.add_dest, name='add_dest'),
    path('edit_dest', views.edit_dest, name='edit_dest'),
    path('delete_dest', views.delete_dest, name='delete_dest'),
]