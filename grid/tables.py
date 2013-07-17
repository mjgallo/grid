# tutorial/tables.py
import django_tables2 as tables
from grid.models import Restaurant

class RestaurantTable(tables.Table):
    review = tables.Column("this is the review we want")
    class Meta:
        model = Restaurant
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}