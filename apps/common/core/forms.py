from django import forms


class KeyPrefixForm(forms.Form):
    key_prefix = forms.CharField(
        max_length=6,
        label='Enter first 6 characters of the key'
    )

