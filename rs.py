#!/usr/bin/env python

from __future__ import print_function
import re, string, sys

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

rep = re.compile(r'(\([^\(\)]+\))\^\^(\([^\)]+\))')
ln = re.compile(r'\(\^\^([^\(\)]+)\)')

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

def expand(debug, line):
    while True:
        m = ln.search(line)
        if m is None:
            if debug: print('nothing more to get length of')
            break
        line = line[:m.start()] + str(len(m.group(1))) + line[m.end():]
        if debug: print('result with length expanded: %s' %
                         line.encode('string-escape'))
    while True:
        m = rep.search(line)
        if m is None:
            if debug: print('no more repititions to expand')
            break
        l, r = m.group(1), m.group(2)
        if debug: print('found repition %s^^%s' % (l, r))
        l = l[1:-1]
        line = line[:m.start()] + l*int(r[1:-1]) + line[m.end():]
        if debug: print('result with repitition expanded: %s' %
                         line.encode('string-escape'))
    return line

def run(delim, cmds, debug):
    patterns = []
    macros = {}
    for cmd in cmds:
        if debug: print('reading command %s' % cmd)
        if cmd.startswith('$$'):
            try:
                i = cmd.index('=')
            except:
                sys.exit('invalid macro definition: ' + cmd)
            if debug: print("setting macro '%s' to '%s'" % (cmd[2:i], cmd[i+1:]))
            macros[cmd[2:i]] = cmd[i+1:]
        else:
            pat, repl, conv, flags = get_delim(cmd, delim)
            if debug:
                print('got pattern %s' % pat)
                print('got replacement %s' % repl)
            pat = string.Template(pat).safe_substitute(macros)
            repl = string.Template(repl).safe_substitute(macros)
            if debug:
                print('substituting macros into pattern resulted in %s' % pat)
                print('substituting macros into replacement resulted in %s' %
                      repl)
            patterns.append((re.compile(pat, flags), repl, conv))

    if debug: print('processing input!')

    for line in sys.stdin:
        line = line.rstrip('\n').replace('^^', r'^\^')
        if debug: print('current line: %s' % line)
        for find, replace, conv in patterns:
            if debug: print('applying pattern %s with replacement %s' % (
                                                        find.pattern, replace))
            if conv:
                orig = line
                while True:
                    line = expand(debug, find.sub(replace, line))
                    if line == orig: break
                    if debug:
                        print('converged %s to %s' % (
                                orig.encode('string-escape'),
                                line.encode('string-escape')))
                    orig = line
            else:
                line = expand(debug, find.sub(replace, line))
            if debug:
                print('result of application is %s' %
                        line.encode('string-escape'))
        print(line.replace(r'^\^', '^^'))

def usage():
    print('usage: %s [-h] [-g] [-f] <script/file>' % sys.argv[0], file=sys.stderr)

def main():
    if '-h' in sys.argv:
        usage()
        sys.exit(0)
    use_file = False
    cmds = []
    delim = '/'
    debug = False
    for arg in sys.argv[1:]:
        if arg == '-f':
            if use_file:
                usage()
                sys.exit(1)
            use_file = True
        elif arg.startswith('-d'):
            delim = arg[2:]
        elif arg == '-g':
            debug = True
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
    run(delim, cmds, debug)

if __name__ == '__main__':
    main()
