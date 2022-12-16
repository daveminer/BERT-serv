from django.urls import path

from . import views

urlpatterns = [
    path('', views.post, name='index')
]
