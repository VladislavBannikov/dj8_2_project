from django.db.models import QuerySet
from django.shortcuts import render
from django.db.models import Max, Min
# Create your views here.
# from django.views.generic import TemplateView
from .models import Station, Route
from django.conf import settings


# class StationsView(TemplateView):
#
#     template_name = "routes/stations.html"
#     extra_context = {"center": Station.get_center(),
#                      "stations": Station.objects.all()[1:10],
#                      "routes":Route.objects.all(),
#                      }
#     # {"center": {'x': 55.87767168, 'y': 37.54599654}}

def get_center(stations_qs: QuerySet):
    p = stations_qs.aggregate(long_max=Max('longitude'), long_min=Min('longitude'), lat_max=Max('latitude'),
                              lat_min=Min('latitude'))

    x = p.get('lat_min') + (p.get('lat_max') - p.get('lat_min')) / 2
    y = p.get('long_min') + (p.get('long_max') - p.get('long_min')) / 2

    return {'x': x, 'y': y}


def stations_view(request):
    template_name = "routes/stations.html"
    route_obj = None
    if request.GET.get("route", None) or None:
        route = request.GET.get("route")
        route_obj = Route.objects.get(name=route)
        stations_qs = Station.objects.filter(routes=route_obj)
        center = get_center(stations_qs)
    else:
        stations_qs = [] #Station.objects.all()[:10]
        center = {"x": 55.755814, "y": 37.617635}

    context = {"routes": Route.objects.all(),
               "center": center,
               "stations": stations_qs,
               "route":route_obj,
               "api_key": settings.API_KEY,
               }

    # {"x": 55.698532934999994, "y": 37.5013756258}
    return render(request, template_name, context)
