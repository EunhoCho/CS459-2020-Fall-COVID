from .models import Route
from rest_framework import serializers, viewsets

class RouteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Route
        fields = '__all__'

class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer