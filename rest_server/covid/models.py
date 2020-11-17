from django.db import models

class Route(models.Model):
    userID = models.IntegerField(default=0)
    location_x = models.FloatField(default=0)
    location_y = models.FloatField(default=0)
    datetime = models.DateTimeField()

class Temperature(models.Model):
    userID = models.IntegerField(default=0)
    temperature = models.FloatField(default=36.5)
    datetime = models.DateTimeField()