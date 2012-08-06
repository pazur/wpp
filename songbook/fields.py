from django import forms
from django.forms import widgets

from django.db.models.loading import get_model
from djangotoolbox import fields

class SongListWidgetMixin(object):
    def value_from_datadict(self, data, files, name):
        value = data.get(name, None)
        if not value:
            return None
        return value.split(',')

    def render(self, name, value, attrs=None):
        value = ','.join(str(x) for x in value)
        return super(SongListWidgetMixin, self).render(name, value, attrs)

class SongListWidget(SongListWidgetMixin, widgets.TextInput):
    pass

class SongListHiddenWidget(SongListWidgetMixin, widgets.HiddenInput):
    pass

class SongbookChoiceField(forms.ModelMultipleChoiceField):
    widget = SongListWidget
    hidden_widget = SongListHiddenWidget

    def clean(self, value):
        try:
            return super(SongbookChoiceField, self).clean(value)
        except ValueError as e:
            raise forms.ValidationError(e.message)

class SongListField(fields.ListField):
    def formfield(self, **kwargs):
        db = kwargs.pop('using', None)
        defaults = {
            'form_class': SongbookChoiceField,
            'queryset': get_model('songbook', 'Song').objects.all(),
        }
        defaults.update(kwargs)
        # If initial is passed in, it's a list of related objects, but the
        # MultipleChoiceField takes a list of IDs.
        if defaults.get('initial') is not None:
            initial = defaults['initial']
            if callable(initial):
                initial = initial()
            defaults['initial'] = [i._get_pk_val() for i in initial]
        return super(fields.AbstractIterableField, self).formfield(**defaults)