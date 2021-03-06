from django.utils.html import escape

import yapps.runtime as yapps

class Lexem(object):
    class Verse(object):
        type = 'VERSE'

        def __init__(self, verse, chords=''):
            self.verse = verse.strip()
            self.chords = chords.strip()

        def to_html(self, context):
            return escape(self.verse)

        def __len__(self):
            return len(self.verse)

        def accept(self, visitor):
            visitor.visit_verse(self)

    class Pipe(Verse):
        type = 'PIPE'

    class PipeText(Pipe):
        type = 'PIPETEXT'

        def __init__(self, verse, text, chords=''):
            super(Lexem.PipeText, self).__init__(verse, chords)
            self.text = text.strip()

        def accept(self, visitor):
            visitor.visit_pipe_text(self)

    class EOF(object):
        type = 'EOF'

    class Empty(object):
        type = 'EMPTY'

    class ChorusOpen(object):
        type = 'CHORUS_OP'

    class ChorusClose(object):
        type = 'CHORUS_CL'

CHORDS_SEPARATOR = '$'
PIPE = '|'
TAGS = {
    '<ref>': Lexem.ChorusOpen,
    '</ref>': Lexem.ChorusClose,
}

class Lexer(yapps.Scanner):
    def __init__(self, *args, **kwargs):
        super(Lexer, self).__init__(None, {}, *args, **kwargs)

    def tokenize(self, line):
        for tag in TAGS:
            if tag in line:
                result = ()
                parts = line.split(tag)
                for part in parts:
                    if part.strip():
                        result += self.tokenize(part)
                    result += TAGS[tag](),
                return result[:-1]
        if not line.strip():
            return Lexem.Empty(),
        line = line.replace(u'"', "''")
        verse, chords = (line.split(CHORDS_SEPARATOR, 1) + [''])[:2]
        if not PIPE in verse:
            return Lexem.Verse(verse, chords),
        verse, text = verse.split(PIPE, 1)
        if text.strip():
            return Lexem.PipeText(verse, text, chords),
        return Lexem.Pipe(verse, chords),

    def get_gen(self):
        last = None
        for line in self.input.strip().splitlines():
            for token in self.tokenize(line):
                if not type(last) == Lexem.Empty == type(token):
                    yield token
                last = token
        yield Lexem.EOF()

    def token(self, restrict, context=None):
        if not hasattr(self, '_gen'):
            self._gen = self.get_gen()
        t = self._gen.next()
        return yapps.Token(t.type, t)
