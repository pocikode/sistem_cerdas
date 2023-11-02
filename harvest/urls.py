from django.urls import path

from . import views


app_name = 'harvest'

urlpatterns = [
    path('', views.index, name='index'),
    path('create', views.create, name='create'),
    path('job-<int:job_id>', views.show, name='show'),
]
