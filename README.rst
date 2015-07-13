rs
==

rs is a project I created for two purposes:

- An alternative to sed that's easier to use for simple tasks
- Code golf

The result? A tool with lots of operators and a few fun ways of doing things. Regexes were never this cool. Ever.

`Try it! <http://kirbyfan64.github.io/rs>`_ The sources for the demo page are at the ``gh-pages`` branch. Feel free to open any issues with the page or rs itself on the `bug tracker <http://github/kirbyfan64/rs/issues>`_.

Installation
************

::
   
   python setup.py install

Basics
******

::

   rs.py [-h] [-g] [-f] [-d<delim>] <script or file>

Here's an example usage::

   cat blah | rs.py 'ab/cd'

That's equivalent to the longer::

   cat blah | sed 's/ab/cd/'

The default delimiter is ``/``. To change it, use ``-d``::

   cat blah | rs.py -d: 'ab:cd'

If the delimiter is not preset in the script, the pattern will assumed to be ``^``, and the replacement will be the script::

   echo -e 'a\nb' | rs.py 'xyz'
   # outputs:
   # xyz1
   # xyz2

This can be used to prepend whitespace to a file (useful with Stack Overflow submissions or embedding a file in an rST document).

If the delimiter is present, but the pattern is empty, the pattern wil be ``$``::
   
   echo 'abc' | rs.py '/def'
   # outputs 'abcdef'

Passing ``-g`` will cause rs to print lots and lots of debugging info while reading patterns and expanding the input.

File scripts
************

You can pass ``-f`` to load a file instead::

   echo "ab/cd" > script.rsp
   cat blah | rs.py -f script.rsp

rs scripts end in ``.rsp``.

Lines in a script beginning with `\#` are comments and are ignored.

Operators
*********

Prefixing a pattern with a ``+`` is the convergence operator; I got the feature from the excellent `Retina <https://github.com/mbuettner/retina#retina-is-turing-complete>`_. The convergence operator continuously loops and replaces the pattern until no more substitutions are possible.

Prefixing a pattern with ``*`` makes the pattern case-insensitive.

Prefixing a pattern with ``?`` adds a maximum number of substitutions to the pattern. Only up to that many substitutions will be preformed using that pattern on each line. If the maximum number is over 2 digits long, it *must* be surrounded by brackets. Example::
   
   echo aaa | rs.py '?1a/b'
   # outputs 'baa'
   echo aaaaaaaaaaaa | rs.py '?[11]a/b'
   # outputs bbbbbbbbbbba

Repetition
**********

If you have ``(a)^^(b)``, where ``a`` is some string and ``b`` is an integer, rs will repeat ``a`` ``b`` times. Example::

    (\d)(.)/(\2)^^(\1)

This will replace ``2Z`` with ``ZZ``, ``3#`` with ``###``, ``9%`` with ``%%%%%%%%%``, etc.

Length
******

rs will expand ``(^^a)`` to be the length of ``a``. For instance::

    (\d+)/(^^\1)

will replace ``xx`` with ``2``, ``12323`` with ``5``, and so forth.

Macros
******

Any lines beginning with a double dollar sign (``$$``) will be assumed to be macro definitions. You can define a macro and use it later on in your script via the dollar sign. Example::

    $$a=1
    $$b=2
    $a/$b

will replace a ``1`` with a ``2``.

TODO
****

- States. Something so that I can create a state using ``$^x`` and jump to it if a pattern matches.
