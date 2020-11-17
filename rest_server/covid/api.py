from .models import Route
from .models import Temperature
from rest_framework import serializers, viewsets

class RouteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Route
        fields = '__all__'

class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

class TemperatureSerializer(serializers.ModelSerializer):

    class Meta:
        model = Temperature
        fields = '__all__'

class TemperatureViewSet(viewsets.ModelViewSet):
    queryset = Temperature.objects.all()
    serializer_class = TemperatureSerializer