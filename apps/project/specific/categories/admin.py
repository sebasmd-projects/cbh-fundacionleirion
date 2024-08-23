from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin

from .models import AssetCategoryModel

admin.site.register(AssetCategoryModel, ImportExportActionModelAdmin)
