from django.urls import path
from . import views

urlpatterns = [
    path('', views.report, name='report'),
    path('report_data/', views.report_data, name='report_data')
]