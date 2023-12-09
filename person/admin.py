from django.contrib import admin
from .models import Person
from import_export.admin import ExportActionMixin

class PersonAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('code', 'name', 'type')
    list_filter = ('type',)  # Add 'type' to enable filtering by person type in admin

admin.site.register(Person, PersonAdmin)