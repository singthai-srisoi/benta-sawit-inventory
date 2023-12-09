from django.contrib import admin
from .models import Destination
from import_export.admin import ExportActionMixin

class DestinationAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('code', 'name')
admin.site.register(Destination, DestinationAdmin)