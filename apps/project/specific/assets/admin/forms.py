from django import forms

from apps.project.specific.assets.models import AssetModel


class AssetModelForm(forms.ModelForm):
    class Meta:
        model = AssetModel
        fields = '__all__'
        widgets = {
            'name': forms.Textarea(attrs={'rows': 2, 'style': 'width: 80%;'}),
            'es_name': forms.Textarea(attrs={'rows': 2, 'style': 'width: 80%;'}),
        }
