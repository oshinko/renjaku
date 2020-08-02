import pathlib
import sys
import webbrowser
import wsgiref.simple_server

workspace = 'www.renjaku.co.jp'


def app(environ, respond):
    if environ['REQUEST_METHOD'] in ('GET', 'HEAD'):
        without_leading_slash = environ['PATH_INFO'][1:]
        path = pathlib.Path(workspace) / without_leading_slash
        if path.is_dir():
            path /= 'index.html'
        if path.is_file():
            respond('200 OK', [])
            return [path.read_bytes()]
    respond('404 Not Found', [])
    return []


if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    httpd = wsgiref.simple_server.make_server('', port, app)
    print(f'Serving {workspace} on port {port}, control-C to stop')
    webbrowser.open(f'http://localhost:{port}')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('Shutting down.')
        httpd.server_close()
