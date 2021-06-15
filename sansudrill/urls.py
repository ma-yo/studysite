from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create_drill', views.create_drill, name='create_drill'),
]