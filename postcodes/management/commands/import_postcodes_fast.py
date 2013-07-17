import sys
import csv

from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand
from django.db import connection, transaction
from psycopg2.extensions import AsIs


from postcodes.models import Postcode

class Command(BaseCommand):
    def handle(self, *args, **options):
        Postcode.objects.all().delete()
        count = 0
        cursor = connection.cursor()
        with open('/Users/mgallo/Envs/env1/mysite/postcodes/management/uk-post-codes-2009abridged.csv') as csvfile: 
            queryList = []
            for row in csv.reader(csvfile):
                try:
                    name = row[0].upper().strip().replace('  ', ' ')
                    location = row[13]) + ' ' + row[14]
                    queryList.append((location, AsIs(name)))
                except ValueError:
                    print "I: skipping %r" % row
                    continue

            query = ("""INSERT INTO postcodes_postcode (location, name) 
                            VALUES (ST_SetSRID(ST_GeomFromText(
                            'POINT%s'),4326), '%s');""")

            cursor.executemany(query, queryList)
            transaction.commit