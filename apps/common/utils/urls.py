from django.urls import path

from .views import robots_txt, set_language

urlpatterns = [
    path('robots.txt', robots_txt),
    path('set_language/', set_language, name='set_language'),
]
