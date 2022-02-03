from csv import reader

from django.core.management.base import BaseCommand

from demencia.models import Region


class Command(BaseCommand):
    help = "load geocodes to DB"

    def handle(self, *args, **options):
        with open("geocodes.csv", encoding="utf-8") as f:
            geocodes_reader = reader(f)
            for row in geocodes_reader:
                geocode, name = row
                Region.objects.get_or_create(geocode=geocode, name=name)
