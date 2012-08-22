# -*- encoding:utf-8 -*-

import urllib2

import bs4


class SongImporter(object):
    def __init__(self, url, version=1):
        conn = urllib2.urlopen(url)
        src = conn.read()
        conn.close()
        self.version = version - 1
        self.soup = bs4.BeautifulSoup(src)

    def get(self):
        return {
            'lyrics': self.get_lyrics(),
            'title': self.get_title(),
            'subtitle': self.get_subtitle(),
            'music_author': self.get_music_author(),
            'lyrics_author': self.get_lyrics_author(),
            'year': self.get_year(),
            'info': self.get_info()
        }

    def get_lyrics(self):
        try:
            root = self.soup.find(attrs={'id': 'wariant%d' % self.version})
            result = u''
            verses = root.children
            verses.next()  # Skip line "wariant 3"
            for verse in verses:
                if 'object_spacebefore' in verse.attrs.get('class', []):
                    result += u'\n'
                result += verse.children.next()
                result += u'\n'
            return result
        except (AttributeError, StopIteration):
            return None

    def get_title(self):
        try:
            title_text = self.soup.find(text=u'Tytuł')
            title_node = title_text.parent
            return title_node.find_next_sibling().children.next()
        except (AttributeError, StopIteration):
            return None

    def get_subtitle(self):
        try:
            title_text = self.soup.find(text=u'Tytuł')
            title_node = title_text.parent
            node = title_node.find_next_sibling().find_next_sibling()
            if 'object_color' not in node.attrs.get('class', []):
                return node.children.next()
        except (AttributeError, StopIteration):
                return None

    def get_first_from_left_sidebar(self, text):
        try:
            author_text = self.soup.find(text=text)
            author_node = author_text.parent
            node = author_node.find_next_sibling()
            result = node.stripped_strings.next()
            if result == u'nieznany':
                return None
            return result
        except (AttributeError, StopIteration):
            return None

    def get_lyrics_author(self):
        return self.get_first_from_left_sidebar(u'Autor słów')

    def get_music_author(self):
        return self.get_first_from_left_sidebar(u'Autor muzyki')

    def get_year(self):
        return self.get_first_from_left_sidebar(u'Data powstania')

    def get_info(self):
        try:
            text = self.soup.find(text=u'Informacje dodatkowe')
            p_node = text.parent
            info_div = p_node.find_next_sibling()
            first_paragraph = info_div.children.next()
            result = u''
            for string in first_paragraph.strings:
                if not string.strip().startswith(u'[') and string.strip() != u',':
                    result = result + string
            return result
        except (AttributeError, StopIteration):
            return None
