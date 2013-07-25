import sys, os
import csv


from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand

from postcodes.models import Postcode

class Command(BaseCommand):
    def handle(self, *args, **options):
        Postcode.objects.all().delete()
        count = 0
        with open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'uk-post-codes-2009.csv'))) as csvfile: 
            for row in csv.reader(csvfile):
                try:
                    name = row[0].upper().strip().replace('  ', ' ')
                    location = Point(map(float, row[13:15]))
                except ValueError:
                    print "I: skipping %r" % row
                    continue

                Postcode.objects.create(name=name, location=location)

                count += 1
                if count % 10000 == 0:
                    print "Imported %d" % count