import sys
import logging
import re


def main(ifile=sys.stdin):
    """Main entrypoint for CC-CEDICT parser"""
    for line in ifile:
        line = line.strip()

        # Skip the comments
        if line.startswith('#'):
            continue

        fields = line.split(' ', 2)

        # Skip any malformed lines.
        if len(fields) != 3:
            logging.warning('Skipped a malformed line: %s', line)
            continue

        word_tr, word_sp, others = fields


if __name__ == '__main__':
    main()
