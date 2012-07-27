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
    comment = models.TextField()
    lyrics_author = models.CharField(max_length=255)
