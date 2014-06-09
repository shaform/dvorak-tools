#!/usr/bin/env python
# xrdpkeymap_qwerty_to_dvorak.py
"""
Usage: python xrdpkeymap_qwerty_to_dvorak.py km-input.ini > km-output.ini
"""
import fileinput
import re

# keycodes
# $ xmodmap -pk for current mapping
# ref: http://forums.fedoraforum.org/showthread.php?t=265100
QWERTY = (
        20, 21,
        24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35,
        38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48,
        52, 53, 54, 55, 56, 57, 58, 59, 60, 61
        )

DVORAK = (
        34, 35,
        48, 59, 60, 33, 29, 41, 42, 54, 27, 46, 61, 21,
        38, 32, 26, 30, 31, 40, 43, 28, 57, 39, 20,
        47, 24, 44, 45, 53, 56, 58, 25, 55, 52
        )

TRANS_DICT = dict(zip(QWERTY, DVORAK))


re_title = re.compile('\[.*\]\n')
re_keydef = re.compile('Key(\d+)=(.*)\n')
buf = []
buf_dict = {}

def output_keydefs():
    global buf, buf_dict
    for k in buf:
        if k in TRANS_DICT:
            print 'Key%d=%s' % (k, buf_dict[TRANS_DICT[k]])
        else:
            print 'Key%d=%s' % (k, buf_dict[k])
    buf = []
    buf_dict = {}


for line in fileinput.input():
        if re_title.match(line) is not None:
            output_keydefs()
            print line,
        elif re_keydef.match(line) is not None:
            m = re_keydef.match(line)
            buf.append(int(m.group(1)))
            buf_dict[int(m.group(1))] = m.group(2)
        else:
            print line,

# output remaining keys
output_keydefs()