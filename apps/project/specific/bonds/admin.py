from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin

from .models import BondModel, BondStatusModel

admin.site.register(BondModel, ImportExportActionModelAdmin)
admin.site.register(BondStatusModel, ImportExportActionModelAdmin)
