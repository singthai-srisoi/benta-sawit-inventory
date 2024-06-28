from django.urls import path
from . import views

urlpatterns = [
    path('customer/', views.customer, name='customer'),
    path('supplier/', views.supplier, name='supplier'),
    path('driver/', views.driver, name='driver'),
    path('add_person/', views.add_person, name='add_person'),
    path('delete_person/', views.delete_person, name='delete_person'),
    path('edit_person/', views.edit_person, name='edit_person'),
    path('api/', views.PersonView.as_view(), name='api_person'),
    path('new/', views.new_person_view, name='new_person'),
]