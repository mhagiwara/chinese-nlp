# coding=utf-8
import sys
from collections import defaultdict
import json


def read_cedict(cedict_file):
    """Read the CC-CEDICT file and returns a dict from word surface form to set of entries."""
    cedict = defaultdict(set)
    for line in cedict_file:
        line = line.strip()
        json_dict = json.loads(line)
        cedict[json_dict['word_sp']].add(line)
        cedict[json_dict['word_tr']].add(line)

    return cedict


def main(ifile=sys.stdin, ofile=sys.stdout, cedict_file=None):
    assert cedict_file

    cedict = read_cedict(cedict_file)

    for line in ifile:
        word, pos, hsk_level = line.decode('utf-8').strip().split('\t')
        cedict_entries = [e for e in cedict[word]
                          if 'variant' not in e and 'surname' not in e]
        if not cedict_entries:
            cedict_entries = ['NO ENTRIES FOUND!!!']
        for entry in cedict_entries:
            ofile.write(u'%s\t%s\t%s\t%s\n' % (word, pos or '', hsk_level, entry))

if __name__ == '__main__':
    import codecs
    main(ofile=codecs.getwriter('utf_8')(sys.stdout),
         cedict_file=codecs.open(sys.argv[1], encoding='utf-8'))
