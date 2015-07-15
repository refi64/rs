tags =
  '&': '&amp;'
  '<': '&lt;'
  '>': '&gt;'

escape = (txt) ->
  txt
    .replace /[&<>]g/, (tag) -> tags[tag] or tag
    .replace /\\n/g, '&#10;'
    .replace /[ ]/g, '&nbsp;'

rsu = 'https://api.github.com/repos/kirbyfan64/rs/contents/rs.py'
status = $ '#status'
out = $ '#output'
window.vm = new PyPyJS()
vm.stdout = vm.stderr = (data) -> out.html out.html() + escape data
status.text 'Loading PyPy.js (this might take a while)...'
vm.ready
  .then ->
    status.text 'Loading rs...'
    rs_req.open 'GET', rsu, true
    rs_req.setRequestHeader 'Accept', 'application/vnd.github.v3.raw+json'
    rs_req.send()
  .then null, (err) ->
    status.text 'ERROR loading PyPy.js: ' + err
    status.css 'color', 'red'

if (query = window.location.href.split('?')[1])?
  query = query.substr(0, query.length-1) if query[query.length-1] == '/'
  query_args = query.split '&'
  for arg in query_args
    [key, val] = arg.split '='
    $("##{key}").text decodeURIComponent val

rs = null
rs_req = new XMLHttpRequest()
string = null
string_req = new XMLHttpRequest()
rs_req.onload = () ->
  if (rs = this.responseText)?
    status.html '<br/>'
    rs = rs.replace 'from __future__ import print_function', ''
    vm.exec """
    from __future__ import print_function
    __name__ = None
    #{rs}
    """
  else status.text 'ERROR loading rs!'

on_error = (err) ->
  out.html out.html() +
    if err.trace?
      escape err.trace
    else 'INTERNAL ERROR: ' + err.toString()
    throw err if not err.trace?

py_escape = (txt) ->
  txt.replace(/\\/g, '\\\\').replace(/\n/g, '\\\\n').replace(/'/g, "\\'")

this.run_code = () ->
  largs = ''
  lines = []
  out.css 'color', 'black'
  out.html ''
  lines = $('#script').val().split(/(?:\n)+/g)
  largs += "'-g', " if $('#debug').prop 'checked'
  largs += lines
    .filter (line) -> line != ''
    .reduce ((a,b) -> "#{a}r'#{py_escape(b)}', "), ''
  on_stdin_ready = () ->
    vm
      .exec """
        from __future__ import print_function
        import sys

        sys.argv = ['rs.py', '', #{largs}]
        main()
        """
      .then null, on_error

  vm
    .exec """
      import sys, cStringIO
      sys.stdin = cStringIO.StringIO('#{py_escape $('#input').val().replace(/^\\n+|\\n+$/g, ''), true}\\n')
      """
    .then on_stdin_ready
    .then null, on_error

  return run_code

this.make_link = () ->
  out = $ '#output'
  out.css 'color', 'black'
  out.html "
  http://kirbyfan64.github.io/rs/index.html?\
  script=#{encodeURIComponent $('#script').val()}\
  &input=#{encodeURIComponent $('#input') .val()}"
