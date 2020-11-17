from rest_framework.decorators import api_view
from rest_framework.response import Response
from .api import RouteSerializer, TemperatureSerializer
from .models import Route, Temperature

@api_view(['GET'])
def route_get(request):
    queryset = Route.objects.all()
    serializers = RouteSerializer(queryset, many=True)
    return Response(serializers.data)

@api_view(['GET'])
def temperature_get(request):
    queryset = Temperature.objects.all()
    serializers = TemperatureSerializer(queryset, many=True)
    return Response(serializers.data)
