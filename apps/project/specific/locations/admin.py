from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from .models import BondLocationModel, LocationModel

admin.site.register(LocationModel, ImportExportActionModelAdmin)
admin.site.register(BondLocationModel, ImportExportActionModelAdmin)
