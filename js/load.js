run_code = (function() {
    var tags = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;'
    };
    function escape(txt) {
        return txt.replace(/[&<>]/g, function(tag) { return tags[tag] || tag; }).replace(/\\n/g, '<br/>').replace(/\n/g, '<br/>');
    }

    var rsu = 'https://api.github.com/repos/kirbyfan64/rs/contents/rs.py';
    var status = document.getElementById('status');
    var out = document.getElementById('output');
    window.vm = new PyPyJS();
    vm.stdout = vm.stderr = function(data) { output.innerHTML += escape(data); }
    status.innerHTML = 'Loading PyPy.js (this might take a while)...'
    vm.ready.then(function() {
        status.innerHTML = 'Loading rs...';
        rs_req.open('GET', rsu, true);
        rs_req.setRequestHeader('Accept', 'application/vnd.github.v3.raw+json');
        rs_req.send();
    }).then(null, function(err) {
        status.innerHTML = 'ERROR loading PyPy.js: ' + err;
        status.style.color = 'red';
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
                document.getElementById('rs_script').value = decodeURIComponent(sides[1]);
                break;
            case 'input':
                document.getElementById('input').value = decodeURIComponent(sides[1]);
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
        if (rs === undefined) status.innerHTML = 'ERROR loading rs!';
        else {
            status.innerHTML = '';
            rs = rs.replace('from __future__ import print_function', '');
            vm.exec('from __future__ import print_function\n__name__=None\n' + rs);
        }
    });

    function on_error(err) {
        if (err.trace !== undefined)
            output.innerHTML += escape(err.trace);
        else
            output.innerHTML += 'INTERNAL ERROR: ' + err.toString();
        output.style.color = 'red';
        if (err.trace === undefined) throw err;
    }

    function py_escape(txt) {
        return txt.replace(/'/g, "\\'").replace(/\n/g, '\\n');
    }

    function run_code() {
        var largs = '';
        var lines = [];
        output.style.color = 'black';
        output.innerHTML = '';
        lines = py_escape(document.getElementById('rs_script').value).split(/(?:\\n)+/g);
        if (document.getElementById('debug').checked)
            largs += "'-g', ";
        for (var i=0; i<lines.length; i++) if (lines[i] != '')
            largs += "r'" + lines[i] + "', ";
        function on_stdin_ready() {
            vm.exec("from __future__ import print_function; import sys; sys.argv = ['rs.py', " + largs + "]\nmain()").then(null, on_error);
        }
        vm.exec("import sys, cStringIO; sys.stdin = cStringIO.StringIO('" + py_escape(document.getElementById('input').value) + "\\n')").then(on_stdin_ready).then(null, on_error);
    }

    return run_code;
})();

function make_link() {
    var out = document.getElementById('output');
    out.innerHTML = 'http://kirbyfan64.github.io/rs/index.html?script=' + encodeURIComponent(document.getElementById('rs_script').value) + '&input=' + encodeURIComponent(document.getElementById('input').value);
}
