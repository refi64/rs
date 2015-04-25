#!/usr/bin/env python

from __future__ import print_function
import re, sys

def get_delim(cmd, delim):
    esc = False
    for i, c in enumerate(cmd):
        if esc: esc = True
        elif c == '\\': esc = False
        elif cmd.startswith(delim, i):
            return cmd[:i], cmd[i+len(delim):]
    return '^', cmd

def run(delim, cmds):
    patterns = []
    for cmd in cmds:
        pat, repl = get_delim(cmd, delim) or 0
        patterns.append((re.compile(pat), repl))

    for line in sys.stdin:
        line = line.rstrip('\n')
        for find, replace in patterns:
            line = find.sub(replace, line)
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
                cmds.extend(f.read().splitlines())
    run(delim, cmds)

if __name__ == '__main__':
    main()
