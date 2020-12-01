from datetime import datetime, timedelta

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from . import route_similarity, notify
from .models import Route, Temperature, User

userID_parameter = openapi.Parameter('userID', openapi.IN_QUERY, description="ID of the user",
                                     type=openapi.TYPE_INTEGER, required=True)
date_parameter = openapi.Parameter('date', openapi.IN_QUERY, description="search date limitation", required=False,
                                   type=openapi.TYPE_INTEGER)


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    http_method_names = ['get', 'post', 'delete']

    @swagger_auto_schema(responses={400: "Invalid Format / No User Found / Invalid Latitude / Invalid Longitude"})
    def create(self, request, *args, **kwargs):
        if 'userID' not in request.data or 'latitude' not in request.data or 'longitude' not in request.data:
            return Response({400: "Invalid Format"})

        userID = request.data['userID']
        data = list(User.objects.filter(id=userID))
        if len(data) == 0:
            return Response({400: "No User Found"})

        latitude = float(request.data['latitude'])
        if latitude > 90 or latitude < -90:
            return Response({400: "Invalid Latitude"})

        longitude = float(request.data['longitude'])
        if longitude > 180 or longitude < -180:
            return Response({400: "Invalid Longitude"})

        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Show the route of the target user'],
                         manual_parameters=[userID_parameter, date_parameter],
                         responses={400: "No User Found / No Route Found"})
    @action(detail=False)
    def user(self, request):
        userID = request.query_params.get('userID')
        data = list(User.objects.filter(id=userID))
        if len(data) == 0:
            return Response({400: "No User Found"}, status=400)

        queryset = self.queryset.filter(userID__exact=userID)
        if request.query_params.get('date'):
            queryset = queryset.filter(datetime__gt=datetime.now() - timedelta(days=int(request.query_params.get('date'))))
        if len(queryset) == 0:
            return Response({400: "No Route Found"}, status=400)

        serializer = RouteSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(tags=['Show the route of the target user if he/she is COVID-19 patient'],
                         manual_parameters=[userID_parameter],
                         responses={400: "No User Found / This user is not COVID patient / No Route Found"})
    @action(detail=False)
    def covidUser(self, request):
        userID = request.query_params.get('userID')
        data = list(User.objects.filter(id=userID))
        if len(data) == 0:
            return Response({400: "No User Found"}, status=400)

        if not data[0].isCOVID:
            return Response({400: "This user is not COVID patient"}, status=400)

        queryset = self.queryset.filter(userID__exact=userID)
        if len(queryset) == 0:
            return Response({400: "No Route Found"}, status=400)

        serializer = RouteSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(tags=['Show the route of all COVID-19 patients'])
    @action(detail=False)
    def allCovidUsers(self, request):
        data = list(User.objects.filter(isCOVID__exact=True))
        target_users = []
        for user in data:
            target_users.append(user.id)
        queryset = self.queryset.filter(userID__in=target_users)
        serializer = RouteSerializer(queryset, many=True)
        return Response(serializer.data)


class TemperatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Temperature
        fields = '__all__'


class TemperatureViewSet(viewsets.ModelViewSet):
    queryset = Temperature.objects.all()
    serializer_class = TemperatureSerializer
    http_method_names = ['get', 'post', 'delete']

    @swagger_auto_schema(responses={400: "Invalid Format / No User Found / Invalid Temperature"})
    def create(self, request, *args, **kwargs):
        if 'userID' not in request.data or 'temperature' not in request.data:
            return Response({400: "Invalid Format"})

        userID = request.data['userID']
        data = list(User.objects.filter(id=userID))
        if len(data) == 0:
            return Response({400: "No User Found"})

        temperature = float(request.data['temperature'])
        if temperature > 60 or temperature < 0:
            return Response({400: "Invalid Temperature"})

        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Show the temperature of the target user'],
                         manual_parameters=[userID_parameter],
                         responses={400: "No User Found / No Temperature Record Found"})
    @action(detail=False)
    def user(self, request):
        userID = request.query_params.get('userID')
        data = list(User.objects.filter(id=userID))
        if len(data) == 0:
            return Response({400: "No User Found"}, status=400)

        target_userID = userID
        queryset = self.queryset.filter(userID__exact=target_userID)
        if len(queryset) == 0:
            return Response({400: "No Temperature Record Found"}, status=400)

        serializer = TemperatureSerializer(queryset, many=True)
        return Response(serializer.data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'delete']

    @swagger_auto_schema(tags=['Show the current COVID-19 patients'])
    @action(detail=False)
    def covid(self, request):
        queryset = self.queryset.filter(isCOVID__exact=True)
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(tags=['Set user to COVID-19 patient'],
                         manual_parameters=[userID_parameter],
                         responses={400: "No User Found"})
    @action(detail=False)
    def setCovid(self, request):
        userID = request.query_params.get('userID')
        data = list(self.queryset.filter(id=userID))
        if len(data) > 0:
            user = data[0]
            user.isCOVID = True
            user.save()
            data = self.queryset.filter(id=userID)
            serializer = UserSerializer(data, many=True)

            for suspect in route_similarity.check_similarity(userID):
                notify.send_notify("코로나바이러스 감염증 19 검사 대상자입니다.")

            return Response(serializer.data, status=200)
        else:
            return Response({400: "No User Found"}, status=400)

    @swagger_auto_schema(tags=['Set user to not COVID-19 patient'],
                         manual_parameters=[userID_parameter],
                         responses={400: "No User Found"})
    @action(detail=False)
    def setCure(self, request):
        userID = request.query_params.get('userID')
        data = list(self.queryset.filter(id=userID))
        if len(data) > 0:
            user = data[0]
            user.isCOVID = False
            user.save()
            data = self.queryset.filter(id=userID)
            serializer = UserSerializer(data, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response({400: "No User Found"}, status=400)
