from django.contrib import admin
from grid.models import Restaurant, Review, GridGroup

class ReviewAdmin(admin.ModelAdmin):
	readonly_fields = ('last_updated',)

admin.site.register(Review, ReviewAdmin)
admin.site.register(Restaurant)
admin.site.register(GridGroup)
