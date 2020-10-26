from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('received', views.received, name='received')
]
