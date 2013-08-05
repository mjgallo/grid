import sys, os
import csv


from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand

from postcodes.models import Postcode

class Command(BaseCommand):
    def handle(self, *args, **options):
        print("running import")
        Postcode.objects.all().delete()
        count = 0
        with open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'mycodes2.csv'))) as csvfile: 
            for row in csv.reader(csvfile):
                try:
                    name = row[0]
                    location = Point(map(float, row[1:3]))
                except ValueError:
                    print "I: skipping %r" % row
                    continue

                Postcode.objects.create(name=name, location=location)

                count += 1
                if count % 1000 == 0:
                    print "Imported %d" % count