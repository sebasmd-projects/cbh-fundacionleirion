from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportActionModelAdmin

from .models import CertificateModel


class CertificateAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = (
        'name',
        'document_number',
        'created',
        'updated'
    )
    search_fields = (
        'id',
        'name',
        'document_number'
    )
    list_filter = ("is_active",)
    fieldsets = (
        (_('Certificate'), {'fields': (
            'name',
            'document_number',
            'is_active'
        )}),
        (_('Dates'), {'fields': (
            'created',
            'updated'
        )}),
        (_('Priority'), {'fields': (
            'default_order',
        )}),
    )
    readonly_fields = (
        'created',
        'updated'
    )
    


admin.site.register(CertificateModel, CertificateAdmin)
