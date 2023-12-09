from django.contrib import admin
from .models import Vehicle
from import_export.admin import ExportActionMixin

class VehicleAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('reg_no', 'model')
    list_filter = ('model',)
admin.site.register(Vehicle, VehicleAdmin)