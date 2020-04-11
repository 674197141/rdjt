# -*- coding: utf-8 -*-
from app import app
# -*- coding: utf-8 -*-
from app import app
from tornado.ioloop import IOLoop
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
import os
import tornado.log
from tornado.options import options, define
import logging
import sys

options.log_file_prefix = os.path.join(os.path.dirname(__file__), 'logs/api_log')


class LogFormatter(tornado.log.LogFormatter):
    def __init__(self):
        super(LogFormatter, self).__init__(
            fmt='%(color)s[%(asctime)s %(filename)s:%(funcName)s:%(lineno)d %(levelname)s]%(end_color)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')


def main():
    tornado.options.parse_command_line()
    [i.setFormatter(LogFormatter()) for i in logging.getLogger().handlers]
    http_server = HTTPServer(WSGIContainer(app))
    if sys.platform == 'win32':
        http_server.listen(app.config['API_PORT'])
    else:
        http_server.bind(app.config['API_PORT'], app.config['API_HOST'])
        http_server.start(5)
    IOLoop.instance().start()


if __name__ == '__main__':
    main()
# app.run(app.config['API_HOST'], port=app.config['API_PORT'], debug=app.config['DEBUG'])
