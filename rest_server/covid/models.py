from django.db import models


class Route(models.Model):
    userID = models.IntegerField(default=0)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    datetime = models.DateTimeField()


class Temperature(models.Model):
    userID = models.IntegerField(default=0)
    temperature = models.FloatField(default=36.5)
    datetime = models.DateTimeField()


class User(models.Model):
    isCOVID = models.BooleanField(default=False)
    email = models.CharField(default='', max_length=255)
