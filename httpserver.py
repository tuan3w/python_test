#!/usr/bin/python


from SocketServer import TCPServer, StreamRequestHandler as RH
import socket
import re
import os
import urlparse

HOST = 'localhost'
PORT = 1234
ADDR = (HOST, PORT)


class MyServer(TCPServer):
    def __init__(self, server_address, request_class_handler):
        TCPServer.__init__(self, server_address, request_class_handler)



class MimeType:
    files = '/etc/mime.types'
    mime_map = None
    def __init__(self):
        if not MimeType.mime_map:
            self.setup()

    def setup(self):
        f = open(self.files, 'r')
        for line in f:
            words = line.strip().split()

            if len(words) > 1:
                self.add_mimetype(words[0], words[1:])
    def add_mimetype(self, mime, exts):
        if not MimeType.mime_map:
            MimeType.mime_map = {}

        for ext in exts:
            MimeType.mime_map['.' +ext] = mime

    def get_mime_type(self,ext):
        return MimeType.mime_map[ext]




class MyRequestHandler(RH):
    DEFAULT_ROOT = '.'
    def handle(self):
        first_line = self.rfile.readline()
        querys = first_line.split()
        file_path = querys[1]

        ext = os.path.splitext(file_path)[1]
        mime_tool = MimeType()
        mime_type = mime_tool.get_mime_type(ext)
        print mime_type
        if file_path.startswith('/'): file_path = file_path[1:]

        path = os.path.join(os.path.abspath(self.DEFAULT_ROOT), file_path)
        print 'path: ', path
        if os.path.isfile(path):
            try:
                f = open(path, 'r')
                self.wfile.write('HTTP/1.1 200 OK\r\n')
                self.wfile.write('Server: %s\r\n' % 'PyS0.1(LinuxMint)')
                self.wfile.write('Content-Type:%s\r\n' % mime_type)
                self.wfile.write('\r\n')

                self.wfile.write(f.read())

            except IOError:
                print 'error while reading resource'
                self.request.close()

    def process_request_deprecate(self, request, client_address):
        print 'a connection from ...', client_address
        while True:
            try:
                self.finish_request(request, client_address)
            except socket.error:
                print 'error', socket.error
                self.shutdown_request(request)

if __name__ == '__main__':
    server = MyServer(ADDR, MyRequestHandler)
    server.serve_forever()
