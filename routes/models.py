from django.db import models
from django.db.models import Max, Min


# from django.contrib.gis.geos import Point


# Create your models here.


class Station(models.Model):
    latitude = models.FloatField(verbose_name='latitude')
    longitude = models.FloatField(verbose_name='longitude')
    routes = models.ManyToManyField("Route", related_name="stations")
    route_numbers = models.CharField(max_length=200,
                                     verbose_name="Routes list")  # excessive but faster, better to have additional relation one to one
    name = models.CharField(max_length=200, verbose_name='station name')

    def __str__(self):
        return self.name


class Route(models.Model):
    name = models.CharField(max_length=300, verbose_name="Route name")

    def __str__(self):
        return self.name
