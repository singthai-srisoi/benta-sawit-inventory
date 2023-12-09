from django.contrib import admin
from .models import Inventory
from import_export.admin import ExportActionMixin

class InventoryAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('ticket_no', 'do')

admin.site.register(Inventory, InventoryAdmin)
