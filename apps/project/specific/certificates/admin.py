from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportActionModelAdmin

from .models import CertificateModel


class CertificateAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = (
        'name',
        'document_type',
        'document_number',
        'step',
        'approved',
        'detail_link',
        'created',
        'updated'
    )
    search_fields = (
        'id',
        'name',
        'document_number'
    )
    list_filter = ("is_active","approved","step","document_type")
    fieldsets = (
        (_('Certificate'), {'fields': (
            'name',
            'document_type',
            'document_number',
            'is_active',
            'step',
            'approved',
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

    def detail_link(self, obj):
        url = reverse('certificates:detail', args=[obj.pk])
        return format_html('<a href="{}">{}</a>', url, obj.pk)


admin.site.register(CertificateModel, CertificateAdmin)
