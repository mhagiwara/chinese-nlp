# coding=utf-8
"""Chinese-to-Chinese conversion library.

This library converts text between Simplified (SP) and Traditional (TR) Chinese.
The conversion algorithm is based on simple maximum-length word segmentation using CC-CEDICT.
"""
import codecs
from collections import Iterator
import simplejson
import unittest


class Trie(object):
    """Simple trie library based on a tree structure. This supports common prefix search
    in addition to adding/finding values.

    This supports arbitrary iterables as keys (e.g., strings, lists, or even iterators.)
    """
    def __init__(self):
        self.children = {}  # dict from an element (in the key Iterable) to sub-trie.
        self.value = None

    def add(self, key, value):
        """Adds a (key, value) pair into this trie.

        Parameters:
            key: Iterable over elements to be used as a key.
            value: An arbitrary object inserted as a value.
        """
        if not isinstance(key, Iterator):
            key = iter(key)

        try:
            elem = next(key)
            self.children.setdefault(elem, Trie()).add(key, value)
        except StopIteration:
            self.value = value

    def find(self, key):
        """Finds a value in this trie using key.

        Parameters:
            key: Iterable over elements to be used as a key.

        Returns:
            Value found. None if key does not exist in this trie.
        """
        if not isinstance(key, Iterator):
            key = iter(key)

        try:
            elem = next(key)
            if elem in self.children:
                return self.children[elem].find(key)
            else:
                return None
        except StopIteration:
            return self.value

    def find_prefix(self, key):
        """Iterates over all the values that are prefixes of key.

        Parameters:
            key: Iterable over elements to be used as a key.

        Returns:
            Iterator over all possible values that are prefixes of the given key.
        """
        if not isinstance(key, Iterator):
            key = iter(key)

        if self.value:
            yield self.value

        try:
            elem = next(key)
            if elem in self.children:
                for prefix in self.children[elem].find_prefix(key):
                    yield prefix
            else:
                return
        except StopIteration:
            pass


class C2CConverter(object):
    """Class for Chinese-to-Chinese conversion."""

    def __init__(self, cedict_path):
        """
        Parameters:
            cedict_path: path (string) to the CC-CEDICT JSON file.
        """
        self.trie_s2t = Trie()
        self.trie_t2s = Trie()

        for line in codecs.open(cedict_path, 'r', encoding='utf-8'):
            json = simplejson.loads(line)
            # Values stored in the trie are pairs (length of the original word, converted word).
            self.trie_s2t.add(json['word_sp'], (len(json['word_sp']), json['word_tr']))
            self.trie_t2s.add(json['word_tr'], (len(json['word_tr']), json['word_sp']))

    def _convert(self, trie, text):
        """A helper method to convert between Simplified and Traditional scripts.

        Parameters:
            trie: Trie object to use for conversion. This is either self.trie_s2t (Sp->Tr) or
                self.trie_t2s (Tr->Sp).
            text: Text to convert.

        Returns:
            Converted text (string).
        """
        if not text:
            return ''

        entries = list(trie.find_prefix(text))
        if not entries:
            converted = text[0]
            length = 1
        else:
            length, converted = sorted(entries, key=lambda (length, _): -length)[0]

        return converted + self._convert(trie, text[length:])

    def convert_s2t(self, text):
        return self._convert(self.trie_s2t, text)

    def convert_t2s(self, text):
        return self._convert(self.trie_t2s, text)


class C2CConverterTestCase(unittest.TestCase):

    def test_trie(self):
        t = Trie()
        entries = [('A', 15), ('to', 7), ('tea', 3), ('ted', 4), ('ten', 12),
                   ('ten', 12), ('i', 11), ('in', 5), ('inn', 9)]
        for key, value in entries:
            t.add(key, value)

        self.assertEqual(None, t.find('X'))
        for key, value in entries:
            self.assertEqual(value, t.find(key))

        self.assertEqual([], list(t.find_prefix('')))
        self.assertEqual([], list(t.find_prefix('X')))
        self.assertEqual([15], list(t.find_prefix('A')))
        self.assertEqual([11, 5], list(t.find_prefix('in')))
        self.assertEqual([11, 5, 9], list(t.find_prefix('inn')))
        self.assertEqual([11, 5, 9], list(t.find_prefix('innn')))

    def test_c2c_converter(self):
        converter = C2CConverter('cc-cedict/cedict_ts.utf8.20160201.json')
        test_cases = [
            (u'今天天氣很好。', u'今天天气很好。'),
            (u'漢字簡繁轉換', u'汉字简繁转换'),
            (u'面具麵條', u'面具面条'),
            (u'發現頭髮', u'发现头发'),
            (u'回頭發現', u'回头发现'),
            (u'盪鞦韆', u'荡秋千'),
            (u'發點了點頭發了傳真。', u'发点了点头发了传真。')  # fail
        ]

        for tr, sp in test_cases:
            self.assertEqual(sp, converter.convert_t2s(tr))
            self.assertEqual(tr, converter.convert_s2t(sp))

if __name__ == '__main__':
    unittest.main()
