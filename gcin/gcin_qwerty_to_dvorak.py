#!/usr/bin/env python3
# gcin_qwerty_to_dvorak.py
"""
Usage: python gcin_qwerty_to_dvorak.py input.cin > output.cin
"""
import fileinput
import re

QWERTY = '''-=qwertyuiop[]sdfghjkl;'zxcvbn,./_+QWERTYUIOP{}SDFGHJKL:"ZXCVBN<>?'''
DVORAK = '''[]',.pyfgcrl/=oeuidhtns-;qjkxbwvz{}"<>PYFGCRL?+OEUIDHTNS_:QJKXBWVZ'''
TRANS = str.maketrans(QWERTY, DVORAK)


def main():
    re_option = re.compile(r'%(selkey|endkey)\s+(\S+)')
    re_begin = re.compile(r'%\S+\s+begin')
    re_keydef = re.compile(r'^([^#]\S*)(\s+\S+)')
    re_end = re.compile(r'%\S+\s+end')

    begin = False
    for line in fileinput.input():
        # process key definitions
        if begin:
            if re_end.match(line):
                begin = False
            else:
                new_def = re_keydef.subn(
                    lambda x: x.group(1).translate(TRANS) + x.group(2), line)
                # print transformed line
                if new_def[1] != 0:
                    print(new_def[0], end='')
                    continue
            # print comment/end lines
            print(line, end='')
            continue

        m = re_option.match(line)
        if m is not None:
            print('%%%s %s' % (m.group(1), m.group(2).translate(TRANS)))
            continue
        elif re_begin.match(line):
            begin = True
        print(line, end='')


if __name__ == '__main__':
    main()
