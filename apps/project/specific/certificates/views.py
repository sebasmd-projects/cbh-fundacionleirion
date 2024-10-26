from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.generic import (DetailView, FormView, ListView, TemplateView,
                                  View)

from .forms import IDNumberForm
from .models import CertificateModel


class CertificateFormFacadeTemplateView(TemplateView):
    template_name = 'certificate_form_facade.html'


class LockoutTimeView(View):
    def get(self, request):
        lockout_time = request.session.get('lockout_time')
        if lockout_time:
            lockout_time = timezone.make_aware(
                timezone.datetime.fromtimestamp(lockout_time))
            lockout_duration = timedelta(minutes=60)
            if timezone.now() < lockout_time + lockout_duration:
                remaining_time = (
                    lockout_time + lockout_duration - timezone.now()).seconds
                return JsonResponse({'remaining_time': remaining_time})

        return JsonResponse({'remaining_time': 0})


class CertificateInputView(FormView):
    template_name = 'certificate_input.html'
    form_class = IDNumberForm
    
    def form_valid(self, form):
        max_attempts = 5
        lockout_duration = timedelta(minutes=60)
        failed_attempts = self.request.session.get('failed_attempts', 0)
        lockout_time = self.request.session.get('lockout_time')
        if lockout_time:
            lockout_time = timezone.make_aware(
                timezone.datetime.fromtimestamp(lockout_time))
            if timezone.now() < lockout_time + lockout_duration:
                messages.error(
                    self.request,
                    _('Too many failed attempts.')
                )
                return self.form_invalid(form)
            else:
                self.request.session['failed_attempts'] = 0
                self.request.session['lockout_time'] = None

        document_number = form.cleaned_data['document_number']
        try:
            certificate = CertificateModel.objects.get(
                document_number=document_number)
            self.request.session['failed_attempts'] = 0
            self.request.session['lockout_time'] = None
            return redirect('certificates:detail', pk=certificate.id)

        except CertificateModel.DoesNotExist:
            failed_attempts += 1
            self.request.session['failed_attempts'] = failed_attempts
            if failed_attempts >= max_attempts:
                self.request.session['lockout_time'] = timezone.now(
                ).timestamp()
                messages.error(
                    self.request, _(
                        'Too many failed attempts.'
                    )
                )
            else:
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
        order_by = self.request.GET.get('order_by', 'default_order')
        order_dir = self.request.GET.get('order_dir', 'asc')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(document_number__icontains=search_query)
            )

        if order_dir == 'desc':
            order_by = f'-{order_by}'

        return queryset.order_by(order_by)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_displayed'] = self.get_queryset().count()
        context['order_by'] = self.request.GET.get('order_by', 'default_order')
        context['order_dir'] = self.request.GET.get('order_dir', 'asc')
        return context
