from django.contrib import admin
from grid.models import Restaurant, Review

class ReviewAdmin(admin.ModelAdmin):
	fields = ['reviewer', 'review', 'restaurant',]

admin.site.register(Review, ReviewAdmin)
admin.site.register(Restaurant)
