from csv import reader

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from demencia.models import Region


class Command(BaseCommand):
    help = "load geocodes to DB"

    def handle(self, *args, **options):
        with open("geocodes.csv", encoding="utf-8") as f:
            my_reader = reader(f)
            for row in my_reader:
                geocode, name = row
                try:
                    Region.objects.create(geocode=geocode, name=name)
                except IntegrityError:
                    print(f"{geocode}::{name} уже есть в БД!")
