from django.urls import path
from . import views

urlpatterns=[
    path('', views.index),
    path('visualizer/', views.visualizer),
    path('results/', views.results),
]