# MIT License
#
# Copyright (c) 2017 Evan Liu (hmisty)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

from __future__ import print_function
from socket import socket
import bson

class Proxy:
    remote_functions = []

    def __init__(self, host=None, port=None):
        bson.patch_socket()
        if host != None and port != None:
            self.connect(host, port)

    def connect(self, host, port):
        self.sock = socket()
        self.sock.connect((host, port))

    def __getattr__(self, name): # comes here only if attr not in Proxy
        if name[:8] == 'remote__':
            fn = name[8:]
            self.remote_functions.append(fn)

        return getattr(self.remote_functions, name)

    def invoke_func(self, name):
        def invoke_remote_func(*args):
            self.sock.sendobj({'fn': name, 'args': list(args)})
            return self.sock.recvobj()

        return invoke_remote_func

    def close(self):
        self.sock.close()
        self.sock = None

def connect(host, port):
    proxy = Proxy(host, port)
    return proxy
