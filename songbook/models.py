from django.db import models

class Song(models.Model):
    def to_spreadsheet(self):
        return {
            'title': self.title,
            'lyrics': self.lyrics,
        }
    spreadsheet_fields = ['title', 'lyrics']

    title = models.CharField(max_length=255)
    lyrics = models.TextField()
    comment = models.TextField(blank=True, null=True)
    info = models.TextField(blank=True, null=True)
    lyrics_author = models.CharField(max_length=255, blank=True, null=True)
    music_author = models.CharField(max_length=255, blank=True, null=True)
    music_year = models.SmallIntegerField(blank=True, null=True)
    lyrics_year = models.SmallIntegerField(blank=True, null=True)
