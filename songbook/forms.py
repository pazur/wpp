from django import forms
from django.forms.models import ModelForm

from songbook import models


class SongbookForm(ModelForm):
    #songs = forms.ModelMultipleChoiceField(queryset=models.Song.objects.all())

    class Meta:
        model = models.SongBook
        #exclude = ('songs',)
        #widgets =

class SongForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SongForm, self).__init__(*args, **kwargs)
        self.fields['lyrics'].widget.attrs['rows'] = '20'
        self.fields['lyrics'].widget.attrs['cols'] = '80'
        self.fields['info'].widget.attrs['rows'] = '5'
        self.fields['info'].widget.attrs['cols'] = '80'
        self.fields['comment'].widget.attrs['rows'] = '5'
        self.fields['comment'].widget.attrs['cols'] = '80'


    class Meta:
        model = models.Song
