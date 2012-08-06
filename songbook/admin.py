from django.contrib import admin

from songbook import models

class SongBookAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.Song)
admin.site.register(models.SongBook)