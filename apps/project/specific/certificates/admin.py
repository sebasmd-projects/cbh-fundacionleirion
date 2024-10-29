from django.contrib import admin, messages
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
    list_filter = ("is_active", "approved", "step", "document_type")
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
    list_per_page = 100
    max_list_per_page = 2000

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['list_per_page_options'] = [10, 50, 100, 1000]

        list_per_page_value = request.GET.get('list_per_page')
        if list_per_page_value:
            try:
                list_per_page_value = int(list_per_page_value)
                if list_per_page_value > self.max_list_per_page:
                    messages.warning(
                        request,
                        f"Máximo permitido: {self.max_list_per_page} registros."
                    )
                    list_per_page_value = self.max_list_per_page
                elif list_per_page_value < 1:
                    messages.warning(request, "Mínimo permitido: 1 registro.")
                    list_per_page_value = 1
                self.list_per_page = list_per_page_value
            except ValueError:
                messages.error(request, "Por favor, ingrese un número válido.")
        return super().changelist_view(request, extra_context=extra_context)

    def detail_link(self, obj):
        url = reverse('certificates:detail', args=[obj.pk])
        return format_html('<a href="{}">{}</a>', url, obj.pk)


admin.site.register(CertificateModel, CertificateAdmin)
