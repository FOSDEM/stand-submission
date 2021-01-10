from rest_framework import viewsets, permissions
from .serializers import *
from review.models import Decision
from .models import Theme


class ThemeViewSet(viewsets.ModelViewSet):
    queryset = Theme.objects.all()
    serializer_class = ThemeViewSerializer
    http_method_names = ['get', 'head']


class DecisionViewSet(viewsets.ModelViewSet):
    queryset = Decision.objects.filter(accepted=True)
    serializer_class = DecisionSerializer
    http_method_names = ['get', 'head']


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Decision.objects.filter(accepted=True)
    serializer_class = ContactDecisionSerializer
    http_method_names = ['get', 'head']
    permission_classes = [permissions.IsAuthenticated]
