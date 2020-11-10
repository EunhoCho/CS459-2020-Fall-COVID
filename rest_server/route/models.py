from django.db import models

class Route(models.Model):
    location_x = models.FloatField(default=0)
    location_y = models.FloatField(default=0)
    datetime = models.DateTimeField()