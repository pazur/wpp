from collections import defaultdict
from yapps import runtime

from django.utils.html import escape

from songbook.export import grammar, lexer

class Exporter(object):
    def __init__(self, song):
        self.song = song

    def parse_lyrics(self):
        parser = grammar.Lyrics(lexer.Lexer(self.song.lyrics))
        return parser.entry()

    def get_params(self):
        mapping = {
            'lyrics_author': 'lyrics',
            'music_author': 'music',
            'lyrics_year': 'lyricsyear',
            'music_year': 'musicyear',
            'alt_title': 'alt',
        }
        result = {}
        for key in mapping:
            value = getattr(self.song, key)
            if value:
                result[mapping[key]] = value
        if not result:
            return ''
        return '[%s]' % ','.join('%s=%s' % item for item in result.iteritems())


    def get_info(self):
        if not self.song.info:
            return ''
        return "\n\\begin{info}%s\\end{info}" % self.song.info

    def get_lyrics(self):
        tree = self.parse_lyrics()
        context = defaultdict(lambda: defaultdict(list))
        return tree.to_latex(context)

    def export(self):
        params = self.get_params()
        title = self.song.title
        info = self.get_info()
        lyrics = self.get_lyrics()
        return "\\song%s\n{%s}%s\n%s\n\n" % (params, title, info, lyrics)

    def export_or_error(self):
        try:
            return self.export()
        except runtime.SyntaxError as e:
            return 'LYRICS PARSE ERROR: %s' % e.msg

class HtmlExporter(object):
    def __init__(self, song):
        self.song = song

    def parse_lyrics(self):
        parser = grammar.Lyrics(lexer.Lexer(self.song.lyrics))
        return parser.entry()

    def get_lyrics(self):
        tree = self.parse_lyrics()
        return tree.to_html({})

    def export(self):
        return self.get_lyrics()

    def export_or_error(self):
        try:
            return self.export()
        except runtime.SyntaxError as e:
            return "<div class='error'>%s</div>" % escape('LYRICS PARSE ERROR: %s' % e.msg)