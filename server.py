#  coding: utf-8 
import socketserver
import os
import mimetypes

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
        print ("Got a request of: %s\n" % self.data)
        client_request = self.data.decode("utf-8").split()
        #print(client_request)

        path = client_request[1]
        if client_request[0] != "GET":
            respone = "HTTP/1.1 405 Method Not Allowed\r\n"
            self.request.sendall(respone.encode("utf-8"))
        else:
            raw_path = os.path.abspath("www" + path)
            path_split = path.split('.')
            print(raw_path)
            if (len(path_split)==1 and path[-1]!='/'): #If not a file and not ending with "/" and doesn't exist
                respone = "HTTP/1.1 301 Moved Permanently\r\nLocation: " + path + "/\r\n\r\n301 Moved Permanently" 
                print(respone)
                self.request.sendall(respone.encode("utf-8"))
                return #################################
            
            print(raw_path)
            if os.path.exists(raw_path):
                if os.path.isdir(raw_path):
                    print('its a dir')
                    raw_path = os.path.abspath(raw_path + "/index.html")

                #Should be a file now   
                if os.path.exists(raw_path) and os.path.isfile(raw_path):
                    filename = os.path.normpath(raw_path).split(os.path.sep)[-1]
                    fieltype = mimetypes.guess_type(filename)[0]
                    
                    try:
                        file = open(raw_path, "rb")
                    except:
                        self.send_404()
                        return

                    file_content = file.read()
                    respone = "HTTP/1.1 200 OK\r\nContent-Type: " + str(fieltype) + "\r\n\r\n"
                    print(respone)
                    self.request.sendall(respone.encode("utf-8"))
                    print('sending file content')
                    self.request.send(file_content)

                else: #If a given directory does not have index.html
                    self.send_404()
            else:
                self.send_404()

    def send_404(self):
        respone = "HTTP/1.1 404 Not Found\r\n"
        self.request.sendall(respone.encode("utf-8"))                







if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
