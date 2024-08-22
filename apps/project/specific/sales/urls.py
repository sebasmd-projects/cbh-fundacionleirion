from django.urls import path

from .views import SalesView

urlpatterns = [
    path(
        'sales/',
        SalesView.as_view(),
        name='sales_view'
    )
]
