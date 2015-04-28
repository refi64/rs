#!/usr/bin/env python

from __future__ import print_function
import re, sys

# XXX: this sucks
import sre_parse
orig_expand_template = sre_parse.expand_template
def wrap_expand_template(template, match):
    class MatchWrapper(object):
        def __init__(self):
            self.string = match.string
        def group(self, n):
            return match.group(n) or self.string[:0]
    return orig_expand_template(template, MatchWrapper())
sre_parse.expand_template = wrap_expand_template

def get_delim(cmd, delim):
    esc = False
    conv = False
    flags = 0
    if cmd.startswith('+'):
        cmd = cmd[1:]
        conv = True
    if cmd.startswith('*'):
        cmd = cmd[1:]
        flags = re.IGNORE
    for i, c in enumerate(cmd):
        if esc: esc = True
        elif c == '\\': esc = False
        elif cmd.startswith(delim, i):
            return cmd[:i], cmd[i+len(delim):], conv, flags
    return '^', cmd, conv, flags

def run(delim, cmds):
    patterns = []
    rep = re.compile(r'(\([^\)]+\))\^\^(\([^\)]+\))')
    for cmd in cmds:
        pat, repl, conv, flags = get_delim(cmd, delim)
        patterns.append((re.compile(pat, flags), repl, conv))

    for line in sys.stdin:
        line = line.rstrip('\n').replace('^^', '^\^')
        for find, replace, conv in patterns:
            if conv:
                orig = line
                while True:
                    line = find.sub(replace, line)
                    if line == orig: break
                    orig = line
            else:
                line = find.sub(replace, line)
            while True:
                m = rep.search(line)
                if m is None: break
                l, r = m.group(1), m.group(2)
                if l.startswith('(') and l.endswith(')'):
                    l = l[1:-1]
                line = line[:m.start()] + l*int(r[1:-1]) + line[m.end():]
        print(line)

def usage():
    print('usage: %s [-h] [-f] <script/file>' % sys.argv[0], file=sys.stderr)

def main():
    if '-h' in sys.argv:
        usage()
        sys.exit(0)
    use_file = False
    cmds = []
    delim = '/'
    for arg in sys.argv[1:]:
        if arg == '-f':
            if use_file:
                usage()
                sys.exit(1)
            use_file = True
        elif arg.startswith('-d'):
            delim = arg[2:]
        else:
            cmds.append(arg)
    if not cmds:
        print('no commands given', file=sys.stderr)
        usage()
        sys.exit(1)
    if use_file:
        files = cmds
        cmds = []
        for fn in files:
            with open(fn, 'r') as f:
                for line in f:
                    line = line.rstrip('\n')
                    if not line or line.startswith('\\#'): continue
                    cmds.append(line)
    run(delim, cmds)

if __name__ == '__main__':
    main()
