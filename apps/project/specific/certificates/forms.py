import re

from django import forms
from django.utils.translation import gettext_lazy as _

from .models import CertificateModel


class IDNumberForm(forms.Form):

    document_type = forms.ChoiceField(
        label=_("Document Type"),
        choices=CertificateModel.DocumentTypeChoices.choices,
        initial=CertificateModel.DocumentTypeChoices.CC
    )

    document_number = forms.CharField(
        label=_('Document Number'),
        max_length=50
    )

    def clean_document_number(self):
        document_number = self.cleaned_data['document_number']
        document_number = re.sub(r'\D', '', document_number)
        return document_number
