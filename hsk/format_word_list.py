# coding=utf-8

import sys
import re

HSK_STR_TO_LEVEL = {
    u'一级': 1,
    u'二级': 2,
    u'三级': 3,
    u'四级': 4,
    u'五级': 5,
    u'六级': 6
}


def main(ifile=sys.stdin, ofile=sys.stdout):
    """Main entrypoint HSK word list formatter."""
    for line in ifile:
        line = line.decode('utf-8').strip()
        match = re.match(ur'(.*?)(?:（(.*?)）)?（([一二三四五六]级)）', line)
        if match:
            word = match.group(1)
            pos = match.group(2)
            hsk_level = HSK_STR_TO_LEVEL[match.group(3)]
            ofile.write('%s\t%s\t%s\n' % (word, pos or '', hsk_level))

if __name__ == '__main__':
    import codecs
    main(ofile=codecs.getwriter('utf_8')(sys.stdout))
