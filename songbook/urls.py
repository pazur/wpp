from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('songbook.views',
    url(r'^add_song/', 'song_create_view', name="add_song"),
    url(r'^update_song/(?P<pk>[0-9]+)/$', 'song_update_view', name="update_song"),
    url(r'^song/(?P<pk>[0-9]+)/$', 'song_detail_view', name="song"),
    url(r'^song/(?P<pk>[0-9]+)/latex/$', 'song_latex_view', name="song_latex"),
    url(r'^song_list/$', 'song_list_view', name="song_list"),

    url(r'^add_songbook/', 'songbook_create_view', name="add_songbook"),
    url(r'^update_songbook/(?P<pk>[0-9]+)/$', 'songbook_update_view', name="update_songbook"),
    url(r'^songbook/(?P<pk>[0-9]+)/$', 'songbook_detail_view', name="songbook"),
    url(r'^songbook_list/$', 'songbook_list_view', name="songbook_list"),
)
