# -*- coding: utf-8 -*-
import os


class BaseCase(object):

    def handle_file(self, handler, full_path):
        try:
            with open(full_path, 'rb') as reader:
                content = reader.read()
            handler.send_content(content)
        except IOError as msg:
            msg = "'{0}' cannot be read: {1}".format(full_path, msg)
            handler.handle_error(msg)

    def index_path(self, handler):
        return os.path.join(handler.full_path, 'index.html')

    def test(self, handler):
        assert False, 'Not implemented'

    def act(self, handler):
        assert False, 'Not implemented'


class CaseNoFile(BaseCase):

    def test(self, handler):
        return not os.path.exists(handler.full_path)

    def act(self, handler):
        raise ServerException("'{0}' not found".format(handler.path))


class CaseCGIFile(BaseCase):

    def test(self, handler):
        return os.path.isfile(handler.full_path) and \
                handler.full_path.endswith('.py')

    def act(self, handler):
        self.run_cgi(handler, handler.full_path)

    def run_cgi(self, handler, full_path):
        cmd = 'python3 ' + full_path
        child_out = os.popen(cmd)
        data = child_out.read()
        child_out.close()
        handler.send_content(data)


class CaseExistingFile(BaseCase):

    def test(self, handler):
        return os.path.isfile(handler.full_path)

    def act(self, handler):
        self.handle_file(handler, handler.full_path)


class CaseAlwaysFail(BaseCase):

    def test(self, handler):
        return True

    def act(self, handler):
        raise ServerException("Unknown object '{0}'".format(handler.path))


class CaseDirectoryIndexFile(BaseCase):

    def test(self, handler):
        return os.path.isdir(handler.full_path) and \
                os.path.isfile(self.index_path(handler))

    def act(self, handler):
        self.handle_file(handler, self.index_path(handler))


class CaseDirectoryNoIndexFile(BaseCase):

    LIST_PAGE = '''\
    <html>
    <body>
    <ul>
    {0}
    </ul>
    </body>
    </html>
    '''

    def test(self, handler):
        return os.path.isdir(handler.full_path) and \
               not os.path.isfile(self.index_path(handler))

    def act(self, handler):
        self.list_dir(handler, handler.full_path)

    def list_dir(self, handler, full_path):
        try:
            entries = os.listdir(full_path)
            bullets = ['<li>{0}</li>'.format(e)
                       for e in entries if not e.startswith('.')]
            page = self.LIST_PAGE.format('\n'.join(bullets))
            handler.send_content(page)
        except OSError as msg:
            msg = "'{0}' cannot be listed: {1}".format(full_path, msg)
            handler.handle_error(msg)


class ServerException(Exception):
    pass