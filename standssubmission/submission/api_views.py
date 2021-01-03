from rest_framework import viewsets
from .serializers import *
from review.models import Decision


class DecisionViewSet(viewsets.ModelViewSet):
    queryset = Decision.objects.filter(accepted=True)
    serializer_class = DecisionSerializer
    http_method_names = ['get', 'head']
