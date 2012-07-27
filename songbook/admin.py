from django.contrib import admin
from django.core.urlresolvers import reverse
from djangoappengine.storage import prepare_upload

from songbook import models

class SongAdmin(admin.ModelAdmin):
    def add_view(self, request, form_url='', extra_context=None):
        if request.method == 'GET':
            view_url = reverse('admin:songbook_song_add')
            extra_context = extra_context or {}
            upload_url, upload_data = prepare_upload(request, view_url)
            extra_context['upload_url'] = upload_url
            extra_context['upload_data'] = upload_data
            form_url = upload_url
        return super(SongAdmin, self).add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, extra_context=None):
        return super(SongAdmin, self).change_view(request, object_id, extra_context)

admin.site.register(models.Song, SongAdmin)
