// XXX: I need to add more line breaks!

run_code = (function() {
    var tags = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;'
    };
    function escape(txt) {
        return txt.replace(/[&<>]/g, function(tag) { return tags[tag] || tag; }).replace(/\n/g, '<br/>').replace(/ /g, '&nbsp;');
    }

    var rsu = 'https://api.github.com/repos/kirbyfan64/rs/contents/rs.py';
    var status = $('#status');
    var out = $('#output');
    window.vm = new PyPyJS();
    vm.stdout = vm.stderr = function(data) { out.html(out.html() + escape(data)); }
    status.text('Loading PyPy.js (this might take a while)...');
    vm.ready.then(function() {
        status.text('Loading rs...');
        rs_req.open('GET', rsu, true);
        rs_req.setRequestHeader('Accept', 'application/vnd.github.v3.raw+json');
        rs_req.send();
    }).then(null, function(err) {
        status.text('ERROR loading PyPy.js: ' + err);
        status.css('color', 'red');
    })

    var url_query = window.location.href.split('?')[1];
    if (url_query !== undefined) {
        if (url_query[url_query.length-1] === '/')
            url_query = url_query.substr(0, url_query.length-1);
        var query_args = url_query.split('&');
        for (var i=0; i<query_args.length; i++) {
            var sides = query_args[i].split('=');
            switch (sides[0]) {
            case 'script':
                $('script').text(decodeURIComponent(sides[1]));
                break;
            case 'input':
                $('input').text(decodeURIComponent(sides[1]));
                break;
            }
        }
    }

    var rs = null;
    var rs_req = new XMLHttpRequest();
    var string = null;
    var string_req = new XMLHttpRequest();
    rs_req.onload = (function() {
        rs = this.responseText;
        if (rs === undefined) status.text('ERROR loading rs!');
        else {
            status.html('<br/>');
            rs = rs.replace('from __future__ import print_function', '');
            vm.exec('from __future__ import print_function\n__name__=None\n' + rs);
        }
    });

    function on_error(err) {
        if (err.trace !== undefined)
            out.html(out.html() + escape(err.trace));
        else
            out.html(out.html() + 'INTERNAL ERROR: ' + err.toString());
        out.css('color', 'red');
        if (err.trace === undefined) throw err;
    }

    function py_escape(txt) {
        return txt.replace(/'/g, "\\'").replace(/\n/g, '\\n');
    }

    function run_code() {
        var largs = '';
        var lines = [];
        out.css('color', 'black');
        out.html('');
        lines = $('#script').val().split(/(?:\n)+/g);
        if ($('#debug').prop('checked'))
            largs += "'-g', ";
        largs += lines.filter(function(line){ return line != ''; }).reduce(function(a,b){ return a + "r'" + py_escape(b) + "', "; }, '');
        function on_stdin_ready() {
            vm.exec("from __future__ import print_function; import sys; sys.argv = ['rs.py', " + largs + "]\nmain()").then(null, on_error);
        }
        vm.exec("import sys, cStringIO; sys.stdin = cStringIO.StringIO('" + py_escape($('#input').val()).replace(/^\\n+|\\n+$/g, '') + "\\n')").then(on_stdin_ready).then(null, on_error);
    }

    return run_code;
})();

function make_link() {
    var out = $('#output');
    out.css('color', 'black');
    out.html('http://kirbyfan64.github.io/rs/index.html?script=' + encodeURIComponent($('#script').val()) + '&input=' + encodeURIComponent($('#input').val()));
}
