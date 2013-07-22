from django.contrib import admin
from grid.models import Restaurant, Review, GridGroup

class ReviewAdmin(admin.ModelAdmin):
	fields = ['reviewer', 'review', 'restaurant', 'good']

admin.site.register(Review, ReviewAdmin)
admin.site.register(Restaurant)
admin.site.register(GridGroup)
