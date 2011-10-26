#!/usr/bin/env python
from __future__ import with_statement
import uuid
import os
from bottle import get, post, run, request, debug, static_file, route

STATIC_PATH = '/home/gfreezy/bottle/upload/static'

@route('/js/:path#.+#')
def server_static(path):
    return static_file(path, root=STATIC_PATH+'/js')


@route('/css/:path#.+#')
def server_static(path):
    return static_file(path, root=STATIC_PATH+'/css')


@route('/pic/:path#.+#')
def server_static(path):
    return static_file(path, root=STATIC_PATH+'/pic')


@post('/upload')
def do_upload():
    if is_xhr():
        filename = request.params.get('qqfile', '')
        save_file(request.body, filename)
        return "{success: true, url: '%s'}" % filename
    else:
        fileobj = request.files.get('qqfile')
        filename = save_file(fileobj.file, fileobj.filename)
        return "{success: true, url: '%s'}" % filename


def is_xhr():
    ''' True if the request was triggered by a XMLHttpRequest. This only
        works with JavaScript libraries that support the `X-Requested-With`
        header (most of the popular libraries do). '''
    requested_with = request.environ.get('HTTP_X_REQUESTED_WITH','')
    return requested_with.lower() == 'xmlhttprequest'


def save_file(filedata, filename):
    if not filedata:
        return
    ext = os.path.splitext(filename)[-1]
    u = str(uuid.uuid1())
    filename = ''.join((u, ext))
    fullpath = os.path.join(STATIC_PATH, 'pic', filename)

    with open(fullpath, 'wb') as f:
        filedata.seek(0)
        f.writelines(filedata)
    
    return filename


@get('/upload')
def upload():
    return '''
<head>
<link rel="stylesheet" type="text/css" href="/css/fileuploader.css" />
<script src="/js/fileuploader.js"></script>
</head>
<body>
<div id="file-uploader">
    <noscript>
        <p>Please enable JavaScript to use file uploader.</p>
        <!-- or put a simple form for upload here -->
    </noscript>
</div>
<script>
var uploader = new qq.FileUploader({
    element: document.getElementById('file-uploader'),
    action: '/upload',
    debug: true
});
</script>
</body>
'''

debug()
run(host='localhost', port=8080)
