rs
==

A little sed-like text replacement tool with full Perl regexes.

Usage
*****

::
   
   rs.py [-h] [-f] [-d<delim>] <script or file>

Here's an example usage::
   
   cat blah | rs.py 'ab/cd'

That's equivalent to the longer::
   
   cat blah | sed 's/ab/cd/'

The default delimiter is '/'. To change it, use ``-d``::
   
   cat blah | rs.py -d: 'ab:cd'

You can pass ``-f`` to load a file instead::
   
   echo "ab/cd" > script
   cat blah | rs.py -f script

If the delimiter is not preset in the script, the pattern will assumed to be ``^``, and the replacement will be the script::
   
   echo -e 'a\nb' | rs.py 'xyz'
   # outputs:
   # xyz1
   # xyz2

This can be used to prepend whitespace to a file (useful with Stack Overflow submissions or embedding a file in an rST document).