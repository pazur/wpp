from django import forms
from django.forms.models import ModelForm

from songbook import models


class SongbookForm(ModelForm):
    #songs = forms.ModelMultipleChoiceField(queryset=models.Song.objects.all())

    class Meta:
        model = models.SongBook
        #exclude = ('songs',)
        #widgets =