from django import forms
import re
from django.utils.translation import gettext_lazy as _

class IDNumberForm(forms.Form):
    document_number = forms.CharField(label=_('ID Number'), max_length=50)

    def clean_document_number(self):
        document_number = self.cleaned_data['document_number']
        document_number = re.sub(r'\D', '', document_number)
        return document_number
