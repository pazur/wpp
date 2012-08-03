from yapps import runtime

from songbook.export import grammar, lexer

class Exporter(object):
    def __init__(self, song):
        self.song = song

    def parse_lyrics(self):
        parser = grammar.Lyrics(lexer.Lexer(self.song.lyrics))
        return runtime.wrap_error_reporter(parser, 'entry')

    def export(self):
        pass
        #lyrics_tree = self.parse_lyrics()
