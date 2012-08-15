import re

class Group(object):
    def __init__(self, verses):
        self.verses = verses

    def to_latex(self, context):
        return '\\\\\n'.join(v.to_latex(context) for v in self.verses)

    def to_html(self, context):
        return '</br>'.join(v.to_html(context) for v in self.verses)

class Stanza(object):
    def __init__(self, parts):
        self.parts = parts

    def to_latex(self, context):
        return '\\\\\n'.join(p.to_latex(context) for p in self.parts)

    def to_html(self, context):
        return '<p>%s</p>' % ('</br>'.join(p.to_html(context) for p in self.parts))

class Chorus(Stanza):
    def to_latex(self, context):
        def set_chorus_first_verse(verse):
            context['chorus_first_verse'] = verse.strip(' .?!,:;')
            return verse
        if self.parts:
            context['verse']['first'].insert(0, set_chorus_first_verse)
            return r'\flagverse{Ref.}' + super(Chorus, self).to_latex(context)
        return r'\flagverse{Ref.}' + (context['chorus_first_verse'] or '') + '...'

    def to_html(self, context):
        return '<div class="chorus">%s</div>' % '</br>'.join(p.to_html(context) for p in self.parts)

class Lyrics(object):
    def __init__(self, stanzas):
        self.stanzas = stanzas

    def to_latex(self, context):
        def first_words(verse):
            return re.sub(r'^(.*?)(([\.\?!,:;]+)?)$', r'\\firstwords{\1}\2', verse)
        context['verse']['first'].append(first_words)
        context['verse']['longest'] = ''
        lyrics = '\n\n'.join(s.to_latex(context) for s in self.stanzas)
        pattern = '\\begin{lyrics}[longestline={%s}]\n%s\n\\end{lyrics}'
        return pattern % (context['verse']['longest'], lyrics)

    def to_html(self, context):
        return "\n".join(s.to_html(context) for s in self.stanzas)
