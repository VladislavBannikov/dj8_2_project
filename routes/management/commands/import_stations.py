import csv

from django.core.management.base import BaseCommand
from routes.models import Station, Route


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        all_routes = set()
        all_stations = []
        with open('moscow_bus_stations.csv', 'r', encoding="cp1251") as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            # пропускаем заголовок
            next(reader)

            for line in reader:
                routes = set(i.strip() for i in line[7].split(sep=';'))
                all_routes.update(routes)
                all_stations.append((line[1], float(line[2]), float(line[3]), routes, line[7]))
        Station.objects.all().delete()
        Route.objects.all().delete()

        Route.objects.bulk_create(objs=[Route(name=r) for r in all_routes])
        for st in all_stations:
            station = Station.objects.create(name=st[0], longitude=st[1], latitude=st[2], route_numbers=st[4])
            rr = tuple(r for r in Route.objects.filter(name__in=st[3]))
            station.routes.add(*rr)
            station.save()
