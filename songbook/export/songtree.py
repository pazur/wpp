class Group(object):
    def __init__(self, verses):
        self.verses = verses

    def to_latex(self, context):
        return '\\\\\n'.join(v.to_latex(context) for v in self.verses)

class Stanza(object):
    def __init__(self, parts):
        self.parts = parts

    def to_latex(self, context):
        return '\\\\\n'.join(p.to_latex(context) for p in self.parts) + '\n\n'

class Chorus(Stanza):
    pass

class Lyrics(object):
    def __init__(self, stanzas):
        self.stanzas = stanzas
