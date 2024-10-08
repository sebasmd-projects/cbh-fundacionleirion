from django.urls import path

from .views import CertificateInputView, CertificateDetailView, CertificateListView, CertificateFormFacadeTemplateView

app_name = 'certificates'

urlpatterns = [
    path('certificate/', CertificateInputView.as_view(), name='input'),
    path('certificate/form/', CertificateFormFacadeTemplateView.as_view(), name='form'),
    path('certificate/<uuid:pk>/', CertificateDetailView.as_view(), name='detail'),
    path('certificate/list/', CertificateListView.as_view(), name='list'),
]
