from django.db import models

from songbook.export import Exporter

class Song(models.Model):
    def to_spreadsheet(self):
        return {
            'title': self.title,
            'lyrics': self.lyrics,
        }
    spreadsheet_fields = ['title', 'lyrics']

    title = models.CharField(max_length=255)
    alt_title = models.CharField(max_length=255, verbose_name='alternative title or subtitle', blank=True, null=True)
    lyrics = models.TextField()
    comment = models.TextField(blank=True, null=True)
    info = models.TextField(blank=True, null=True)
    lyrics_author = models.CharField(max_length=255, blank=True, null=True)
    music_author = models.CharField(max_length=255, blank=True, null=True)
    music_year = models.CharField(max_length=255, blank=True, null=True)
    lyrics_year = models.CharField(max_length=255, blank=True, null=True)

    def latex_preview(self):
        return Exporter(self).export_or_error()

    def __unicode__(self):
        return self.title
