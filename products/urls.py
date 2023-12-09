from django.urls import path
from . import views

urlpatterns = [
    path('', views.products, name='products'),
    path('add_product/', views.add_product, name='add_product'),
    path('edit_product/', views.edit_product, name='edit_product'),
    path('delete_product/', views.delete_product, name='delete_product'),
    path('product_types/', views.product_types, name='product_types'),
    path('add_type/', views.add_type, name='add_type'),
    path('edit_type/', views.edit_type, name='edit_type'),
    path('delete_type/', views.delete_type, name='delete_type'),
]