from django.contrib import admin
from .models import *

# Register your models here.
class MovieAdmin(admin.ModelAdmin):
    list_display = ['id',"title", 'movie_id',"movie_type"]
    list_filter = ["title"]

admin.site.register(Movie, MovieAdmin)


# Register your models here.
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["rating", 'comment',"created_at"]

admin.site.register(Review, ReviewAdmin)
