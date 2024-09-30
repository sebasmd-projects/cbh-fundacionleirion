from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.views.generic import DetailView, FormView, ListView

from .forms import IDNumberForm
from .models import CertificateModel
from django.utils.translation import gettext_lazy as _


class CertificateInputView(FormView):
    template_name = 'certificate_input.html'
    form_class = IDNumberForm

    def form_valid(self, form):
        document_number = form.cleaned_data['document_number']
        # Attempt to retrieve the certificate with the sanitized ID number
        try:
            certificate = CertificateModel.objects.get(document_number=document_number)
            return redirect('certificates:detail', pk=certificate.id)
        except CertificateModel.DoesNotExist:
            form.add_error('document_number', _('ID Number not found.'))
            return self.form_invalid(form)


class CertificateDetailView(DetailView):
    model = CertificateModel
    template_name = 'certificate_detail.html'
    context_object_name = 'certificate'


class CertificateListView(PermissionRequiredMixin, ListView):
    model = CertificateModel
    template_name = 'certificate_list.html'
    context_object_name = 'certificates'
    permission_required = ('certificates.view_certificate',)

    def has_permission(self):
        return self.request.user.is_superuser or super().has_permission()

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q', '')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(document_number__icontains=search_query)
            )
        return queryset
