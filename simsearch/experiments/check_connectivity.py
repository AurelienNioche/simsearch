#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  check_connectivity.py
#  simsearch
# 
#  Created by Lars Yencken on 03-09-2010.
#  Copyright 2010 Lars Yencken. All rights reserved.
#
#  Revised by Aurélien Nioche on 23-03-2019

"""
Performs a connectivity check on the search graph, determining how many kanji
occur within the top-k neighbour list of at least one other kanji.
"""

import sys
import optparse

from simsearch import settings
from simsearch import models


def check_connectivity(k=settings.N_NEIGHBOURS_RECALLED):
    kanji_set = models.Node.get_coverage()
    covered_set = set()
    for node in models.Node.objects:
        covered_set.update(n.kanji for n in node.neighbours[:k])

    print(f'{len(covered_set)}/{len(kanji_set)} ({100.0 * len(covered_set) / len(kanji_set):.2f}) covered')


# ---------------------------------------------------------------------------- #


def _create_option_parser():
    usage = \
        """%prog [options]
        
        Performs a connectivity check on the neighbour database to determine how
        many kanji are realistically accessible."""

    parser = optparse.OptionParser(usage)

    parser.add_option(
        '-k', action='store', dest='k', type='int',
        default=settings.N_NEIGHBOURS_RECALLED,
        help='Connected kanji must occur within top-k neighbours [%d]' % settings.N_NEIGHBOURS_RECALLED)

    return parser


def main(argv):
    parser = _create_option_parser()
    (options, args) = parser.parse_args(argv)

    if args:
        parser.print_help()
        sys.exit(1)

    check_connectivity(k=options.k)

# ---------------------------------------------------------------------------- #


if __name__ == '__main__':
    main(sys.argv[1:])
