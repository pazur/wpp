import re

from django.utils.html import escape

from songbook.export import lexer

class Group(object):
    def __init__(self, verses):
        self.verses = verses

    def to_html(self, context):
        verses = '</br>'.join(v.to_html(context) for v in self.verses)
        text = escape(self.verses[-1].text)
        return '<span class="verse-group">%s</span><span>%s</span>' % (verses, text)

    def accept(self, visitor):
        if len(self.verses) == 1:
            visitor.visit_group_single_enter(self)
            for verse in self.verses:
                verse.accept(visitor)
            visitor.visit_group_single_exit(self)
        else:
            visitor.visit_group_enter(self)
            for verse in self.verses:
                verse.accept(visitor)
            visitor.visit_group_exit(self)


class Stanza(object):
    def __init__(self, parts):
        self.parts = parts

    def to_html(self, context):
        return '<p>%s</p>' % ('</br>'.join(p.to_html(context) for p in self.parts))

    def accept(self, visitor):
        visitor.visit_stanza_enter(self)
        for part in self.parts:
            part.accept(visitor)
        visitor.visit_stanza_exit(self)


class Chorus(Stanza):
    def accept(self, visitor):
        if not self.parts:
            visitor.visit_chorus_empty(self)
        else:
            visitor.visit_chorus_enter(self)
            for part in self.parts:
                part.accept(visitor)
            visitor.visit_chorus_exit(self)

    def to_html(self, context):
        return '<div class="chorus">%s</div>' % '</br>'.join(p.to_html(context) for p in self.parts)

class Lyrics(object):
    def __init__(self, stanzas):
        self.stanzas = stanzas

    def accept(self, visitor):
        visitor.visit_lyrics_enter(self)
        for stanza in self.stanzas:
            stanza.accept(visitor)
        visitor.visit_lyrics_exit(self)

    def to_html(self, context):
        return "\n".join(s.to_html(context) for s in self.stanzas)

def id_gen():
    i = 0
    while True:
        yield u'id_%d' % i
        i += 1

class Transformation(object):
    def __init__(self):
        super(Transformation, self).__init__()
        self._disabled = False

    def disable(self):
        self._disabled = True

class FirstVerseTransformation(Transformation):
    def __init__(self):
        super(FirstVerseTransformation, self).__init__()
        self._run = False
        self.disabled = False

    def run(self, value):
        if self._run or self._disabled:
            return value
        self._run = True
        return self.transform(value)

class FirstWordsTransformation(FirstVerseTransformation):
    def transform(self, value):
        return re.sub(r'^(.*?)(([\.\?!,:;]+)?)$', r'\\firstwords{\1}\2', value)

class ChorusFirstWordsTransformation(FirstVerseTransformation):
    def run(self, value):
        return super(ChorusFirstWordsTransformation, self).run(value)

    def transform(self, value):
        return re.sub(r'^(.*?)(([\.\?!,:;]+)?)$', r'\\chorusfirstwords{\1}\2', value)

class Visitor(object):
    def __init__(self):
        self.output = u''
        self.context = {}
        self.states = [{'type': 'none'}]
        self.last_verse_type = None
        self.id_gen = id_gen()

    def push_state(self, state_type, **kwargs):
        state = {'type': state_type}
        state.update(kwargs)
        self.states.append(state)

    def pop_state(self):
        return self.states.pop()

    def get_state(self):
        return self.states[-1]

    def get_output(self):
        return self.output % self.context

    def out(self, text):
        self.output += text.replace(u'%', u'%%')

    def out_raw(self, text):
        self.output += text

    def out_var(self, var_name):
        self.output += u'%%(%s)s' % var_name

    def visit_lyrics_enter(self, lyrics):
        self.push_state('lyrics', transformations=[FirstWordsTransformation()])
        self.longest_line = u''
        self.last_verse_type = ''
        self.out(u'\\begin{lyrics}[longestline={')
        self.out_var(u'longestline')
        self.out(u'}]\n')

    def visit_lyrics_exit(self, lyrics):
        self.pop_state()
        self.context['longestline'] = self.longest_line
        self.out(u'\\end{lyrics}\n')

    def visit_stanza_enter(self, stanza):
        self.push_state('stanza')
        self.last_verse_type = None
        self.out(u'\n')

    def visit_stanza_exit(self, stanza):
        self.pop_state()
        self.last_verse_type = None
        self.out(u'\n')

    def visit_chorus_enter(self, chorus):
        self.push_state('chorus', transformations=[ChorusFirstWordsTransformation()])
        for state in self.states:
            if state['type'] == 'lyrics':
                for transformation in state.get('transformations', []):
                    if isinstance(transformation, FirstWordsTransformation):
                        transformation.disable()
        self.out(u'\n\\begin{chorus}')

    def visit_chorus_exit(self, chorus):
        self.out(u'\\end{chorus}\n')
        self.pop_state()

    def visit_chorus_empty(self, chorus):
        self.out(u'\n\\chorusref\n')

    def visit_group_single_enter(self, group):
        self.push_state('single_group')
        self.print_verse_separator()
        self.last_verse_type = None
        self.out(u'\\markverse[marktext={')
        marktext_id = self.id_gen.next()
        self.out_var(marktext_id)
        self.out(u'}]{')
        self.get_state()['marktext_id'] = marktext_id

    def visit_group_single_exit(self, group):
        self.out(u'}')
        state = self.pop_state()
        self.context[state['marktext_id']] = state['marktext_value']

    def visit_group_enter(self, group):
        self.push_state('group')
        self.print_verse_separator()
        self.last_verse_type = None
        self.out(u'\\begin{markverses}[marktext={')
        marktext_id = self.id_gen.next()
        self.out_var(marktext_id)
        self.out(u'}]%\n')
        self.get_state()['marktext_id'] = marktext_id

    def visit_group_exit(self, group):
        self.last_verse_type = 'new_line'
        self.out(u'\n\\end{markverses}')
        state = self.pop_state()
        self.context[state['marktext_id']] = state['marktext_value']

    def visit_verse(self, verse):
        self.print_verse_separator()
        if len(verse.verse) > len(self.longest_line):
            self.longest_line = verse.verse
        value = verse.verse
        for state in reversed(self.states):
            for transformation in state.get('transformations', []):
                value = transformation.run(value)
        self.out(value)
        self.last_verse_type = 'slashes'

    def visit_pipe_text(self, verse):
        self.visit_verse(verse)
        self.get_state()['marktext_value'] = verse.text

    def print_verse_separator(self):
        if self.last_verse_type is None:
            return
        if self.last_verse_type == 'slashes':
            self.out(u'\\\\*')
        self.out(u'\n')