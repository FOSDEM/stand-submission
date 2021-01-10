from django.urls import path, include
from rest_framework import routers
from . import views, api_views

api_router = routers.DefaultRouter()
api_router.register('accepted', api_views.DecisionViewSet)
api_router.register('themes', api_views.ThemeViewSet)
api_router.register('email', api_views.ContactViewSet)


urlpatterns = [
    path('', views.index, name='index'),
    path('received', views.received, name='received'),
    path('api/', include(api_router.urls))
]
