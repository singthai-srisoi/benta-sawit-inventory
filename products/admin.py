from django.contrib import admin
from .models import Product, ProductType
from import_export.admin import ExportActionMixin

class ProductAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('code', 'name', 'type')
    list_filter = ('type',)

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductType)