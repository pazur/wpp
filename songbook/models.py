from django.core import exceptions
from django.core.urlresolvers import reverse
from django.db import models
from yapps import runtime

from songbook.export import Exporter, HtmlExporter
from songbook import fields


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

    def html_preview(self):
        return HtmlExporter(self).export_or_error()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('song', kwargs={'pk': self.pk})

    def __long__(self):
        return long(self.pk)

    def clean(self):
        super(Song, self).clean()
        try:
            Exporter(self).export()
        except runtime.SyntaxError:
            raise exceptions.ValidationError('Lyrics source is not compiling')

class SongBook(models.Model):
    title = models.CharField(max_length=255)
    song_ids = fields.SongListField(models.ForeignKey(Song))

    def __unicode__(self):
        return self.title

    @property
    def songs(self):
        for id in self.song_ids:
            yield Song.objects.get(id=id)

    def get_absolute_url(self):
        return reverse('songbook', kwargs={'pk': self.pk})
