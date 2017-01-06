import click
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.wsgi import WSGIContainer

from cards import app


@click.command()
@click.option('--port', help='port', default=5000)
def main(port):
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(port=port)
    IOLoop.instance().start()


if __name__ == '__main__':
    main()
