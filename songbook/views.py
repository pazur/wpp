import hmac
import urllib
import urlparse

from django.contrib.auth import decorators
from django.conf import settings
from django.core import exceptions
from django.core.urlresolvers import reverse
from django import http
from django.views.decorators.csrf import csrf_exempt
from django.views import generic
from django.views.generic import detail
from django.utils import simplejson

from importer import bibliotekapiosenki
from songbook import models
from songbook import forms


class SongListView(generic.ListView):
    model = models.Song

class SongUpdateView(generic.UpdateView):
    model = models.Song
    form_class = forms.SongForm

class SongCreateView(generic.CreateView):
    model = models.Song
    form_class = forms.SongForm

    def get_importer_for_url(self, url):
        if urlparse.urlparse(url).netloc.endswith('bibliotekapiosenki.pl'):
            return bibliotekapiosenki.SongImporter
        return None

    def normalize_url(self, url):
        parsed = urlparse.urlparse(url)
        if not parsed.scheme:
            url = u'http://' + url
        return url

    def post(self, request, *args, **kwargs):
        if 'src_url' in request.POST:
            url = self.normalize_url(request.POST['src_url'])
            importer_cls = self.get_importer_for_url(url)
            try:
                version = int(request.POST.get('src_version', 1))
            except ValueError:
                version = 1
            if importer_cls:
                importer = importer_cls(url, version)
                data = importer.get()
                mapping = {
                    'lyrics': 'lyrics',
                    'title': 'title',
                    'subtitle': 'alt_title',
                    'music_author': 'music_author',
                    'lyrics_author': 'lyrics_author',
                    'year': 'lyrics_year',
                    'info': 'info',
                    }
                self.initial = dict((mapping[key], data[key]) for key in mapping)
                if importer.errors:
                    self.extra_context = {'import_errors': importer.errors}
            else:
                self.extra_context = {'import_errors': ('Cannot find importer for url',)}
            request.method = 'get'
            return super(SongCreateView, self).get(request, *args, **kwargs)
        return super(SongCreateView, self).post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SongCreateView, self).get_context_data(**kwargs)
        context['extra_context'] = getattr(self, 'extra_context', None)
        return context

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
        hash = self.request.POST.get('hash', None)
        expected = hmac.new(settings.LATEX_SECRET, request.build_absolute_uri()).hexdigest()
        if hash != expected:
            raise exceptions.PermissionDenied
        if 'songs_only' in self.request.POST:
            songbook = self.get_object()
            return http.HttpResponse(u'\n\n'.join(song.latex_preview() for song in songbook.songs))
        return self.get(request, *args, **kwargs)


class SongbookDetailView(generic.DetailView):
    model = models.SongBook

    def get_context_data(self, **kwargs):
        context = super(SongbookDetailView, self).get_context_data(**kwargs)
        url = reverse('songbook_latex_hash', kwargs={'pk': self.object.pk})
        absolute_url = "http://%s%s" % (self.request.get_host(), url)
        hash = hmac.new(settings.LATEX_SECRET, absolute_url).hexdigest()
        args = urllib.urlencode({'src': absolute_url, 'hash': hash})
        context['pdf_url'] = "%s?%s" % (settings.LATEX_URL, args)
        return context


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
songbook_detail_view = decorators.login_required(SongbookDetailView.as_view())
