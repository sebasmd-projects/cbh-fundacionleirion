import decimal

from cryptography.fernet import Fernet
from django import forms
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView

from .models import SalesModel


class SalesView(LoginRequiredMixin, TemplateView):
    group_required = settings.SALES_GROUP
    redirect_url = "/"
    
    def __init__(self, *args, **kwargs):
        self.cipher = Fernet(settings.ENCODED_KEY)
        super().__init__(*args, **kwargs)

    template_name = 'sales_info.html'

    def decrypt(self, value: str | None):
        if value is None:
            return value

        return self.cipher.decrypt(
            value.encode('utf-8')
        ).decode('utf-8')

    def get(self, request, *args, **kwargs):
        key_prefix = request.session.get('key_prefix', None)
        if not key_prefix:
            return self.render_to_response({'form': KeyPrefixForm()})

        # Validate key prefix
        key: str = settings.SECRET_KEY[:32]
        if not key.startswith(key_prefix):
            return HttpResponse("Invalid key", status=403)

        sales_data = SalesModel.objects.all()

        for sale in sales_data:
            sale.buyer_name = self.decrypt(sale.buyer_name) or ""
            sale.amount_sold = self.decrypt(sale.amount_sold) or ""
            sale.sale_value = self.decrypt(sale.sale_value) or ""

        return self.render_to_response({'sales_data': sales_data})

    def post(self, request, *args, **kwargs):
        form = KeyPrefixForm(request.POST)
        if form.is_valid():
            key_prefix = form.cleaned_data['key_prefix']
            # Validate key prefix
            key = settings.SECRET_KEY[:32]
            if key.startswith(key_prefix):
                request.session['key_prefix'] = key_prefix
                return redirect('sales_view')
            else:
                form.add_error('key_prefix', 'Invalid key')
        return self.render_to_response({'form': form})


class KeyPrefixForm(forms.Form):
    key_prefix = forms.CharField(
        max_length=6,
        label='Enter first 6 characters of the key'
    )
