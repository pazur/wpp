import hmac

from django.contrib.auth import decorators
from django.conf import settings
from django.core import exceptions
from django import http
from django.views.decorators.csrf import csrf_exempt
from django.views import generic
from django.views.generic import detail

from songbook import models


class SongListView(generic.ListView):
    model = models.Song

class SongUpdateView(generic.UpdateView):
    model = models.Song

class SongCreateView(generic.CreateView):
    model = models.Song

class SongDetailView(generic.DetailView):
    model = models.Song

class LatexView(detail.SingleObjectMixin, generic.View):
    def get(self, request, *args, **kwargs):
        object = self.get_object()
        latex = object.latex_preview()
        return http.HttpResponse(latex, mimetype='text/plain; charset=utf-8')

class AllSongsMixin(object):
    def get_context_data(self, **kwargs):
        context = super(AllSongsMixin, self).get_context_data(**kwargs)
        context['all_songs'] = models.Song.objects.all()
        return context

class SongbookUpdateView(AllSongsMixin, generic.UpdateView):
    model = models.SongBook

class SongbookCreateView(AllSongsMixin, generic.CreateView):
    model = models.SongBook

class SongBookLatexHashView(LatexView):
    http_method_names = ['post']
    model = models.SongBook

    def post(self, request, *args, **kwargs):
        hash = sefl.request.POST.get('hash', None)
        expected = hmac.new(settings.LATEX_SECRET, request.build_absolute_uri())
        if hash != expected:
            raise exceptions.PermissionDenied
        return self.get(request, *args, **kwargs)


song_list_view = decorators.login_required(SongListView.as_view())
song_update_view = decorators.login_required(SongUpdateView.as_view())
song_create_view = decorators.login_required(SongCreateView.as_view())
song_detail_view = decorators.login_required(SongDetailView.as_view())

song_latex_view = decorators.login_required(LatexView.as_view(model=models.Song))
songbook_latex_view = decorators.login_required(LatexView.as_view(model=models.SongBook))
songbook_latex_hash_view = csrf_exempt(SongBookLatexHashView.as_view())

songbook_list_view = decorators.login_required(generic.ListView.as_view(model=models.SongBook))
songbook_create_view = decorators.login_required(SongbookCreateView.as_view())
songbook_update_view = decorators.login_required(SongbookUpdateView.as_view())
songbook_detail_view = decorators.login_required(generic.DetailView.as_view(model=models.SongBook))
