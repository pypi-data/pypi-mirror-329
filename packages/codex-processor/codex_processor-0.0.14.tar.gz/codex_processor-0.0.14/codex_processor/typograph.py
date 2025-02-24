#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

NO_BREAK_SEQUENCES = [
    "а",
    "без",
    "в",
    "во",
    "где",
    "для",
    "до",
    "если",
    "среди",
    "за",
    "и",
    "или",
    "из",
    "из-за",
    "из-под",
    "к",
    "ко",
    "как",
    "на",
    "над",
    "не",
    "ни",
    "но",
    "о",
    "об",
    "от",
    "по",
    "под",
    "при",
    "про",
    "с",
    "со",
    "то",
    "у",
    "что",
    "перед",
]

NO_BREAK_SEQUENCES_LEFT = ["бы", "ли", "же", "—", "–"]


def make_set(lst):
    return set(
        lst + list(map(lambda x: x.title(), lst)) + list(map(lambda x: x.upper(), lst))
    )


def typograph(s):
    nbs = make_set(NO_BREAK_SEQUENCES)
    nbsl = make_set(NO_BREAK_SEQUENCES_LEFT)
    for exp in nbs:
        re_from = "([ \u00a0])" + exp + " "
        re_to = "\\1" + exp + "\u00a0"
        s = re.sub(re_from, re_to, s)
    for exp in nbsl:
        re_from = " " + exp + "([ \u00a0])"
        re_to = "\u00a0" + exp + "\\1"
        s = re.sub(re_from, re_to, s)
    return s
