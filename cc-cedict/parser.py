# coding=utf-8
import sys
import logging
import re
import json


def line_to_json(line):
    """Given a single line from CC-CEDICT, turn it a JSON string.

    Returns None if the line is:
        1) Malformed,
        2) Comment
    """
    line = line.decode('utf-8').strip()

    # Skip the comments
    if line.startswith('#'):
        return None

    fields = line.split(' ', 2)

    # Skip any malformed lines.
    if len(fields) != 3:
        logging.warning('Skipped a malformed line: %s', line)
        return None

    word_tr, word_sp, others = fields

    fields = others.split('/')

    # Extract pronunciation in Pinyin
    pinyin_match = re.match(ur'\[([\w :,·]+)\]', fields[0])
    if pinyin_match:
        pinyin = pinyin_match.group(1)
    else:
        logging.warning('Couldn\'t extract Pinyin from line: %s', line)
        pinyin = None

    glosses = [f for f in fields[1:] if f]

    json_dict = {
        'word_tr': word_tr,
        'word_sp': word_sp,
        'pinyin': pinyin,
        'glosses': glosses
    }

    return json.dumps(json_dict, ensure_ascii=False)


def main(ifile=sys.stdin, ofile=sys.stdout):
    """Main entrypoint for CC-CEDICT parser"""
    for line in ifile:
        json_str = line_to_json(line)
        if json_str:
            ofile.write(json_str + '\n')

if __name__ == '__main__':
    import codecs
    main(ofile=codecs.getwriter('utf_8')(sys.stdout))
