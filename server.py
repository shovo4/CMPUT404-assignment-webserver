 #  coding: utf-8 
from code import interact
from ctypes import c_ssize_t
from dataclasses import dataclass
import socketserver

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        self.data = self.data.decode("utf-8")
        illegal = "HTTP/1.1 405 Method Not Allowed\r\n"

        if self.data[0:3] == 'GET':
            self.get(self.data)
                     
            self.request.sendall(bytearray("OK",'utf-8'))
            
        else:
            self.request.send(bytearray(illegal, 'utf-8'))
    
      
    
    def get(self, data):
        index = "index.html"
        css = "text/css"
        #if paths that end in /
        if data.split(" ")[1][-1]=="/":
            self.send(self.data.split(" ")[1]+ index)
        #if paths end with .css
        elif self.data.split(" ")[1][-4:]==".css":
            self.send(self.data.split(" ")[1], css)
        #if paths end with .html
        elif self.data.split(" ")[1][-5:]==".html":
            self.send(self.data.split(" ")[1])
        #if the paths dont end in /
        else:
            self.correctPath(self.data.split(" ")[1])
    
    def send(self,url, contentType="text/html"):
        try:
            file = open("./www"+url)
            data = file.read()
            file.close()
        except:
            response = "HTTP/1.1 404 Not Found\r\n"
            self.request.sendall(bytearray(response, 'utf-8'))
            return
        response = f'HTTP/1.1 200 OK\r\nContent-Type:  {contentType}\r\nContent-Length: {len(data)}\r\n\r\n{data}'
        self.request.sendall(bytearray(response, 'utf-8'))
    
    
    def correctPath(self,url):
        
        try:
            file = open("./www"+url+"/index.html")
            data = file.read()
            file.close()
        except:
            response = 'HTTP/1.1 404 Not Found\r\n'
            self.request.sendall(bytearray(response, 'utf-8'))
            return
        self.response = f'HTTP/1.1 301 Moved Permanently\r\nLocation: {url+"/"}\r\n'
        self.request.sendall(bytearray(self.response, 'utf-8'))
       
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
