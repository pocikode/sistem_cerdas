from django.urls import path

from . import views


app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('tools', views.tools, name='tools'),
    path('check', views.check, name='check'),
]
