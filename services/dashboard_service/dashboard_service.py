#!/usr/bin/python
from http.server import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import json
from cgi import parse_header, parse_multipart, parse_qs

#import sys
#sys.path.insert(0, '../app')
#from Dict import dict


PORT_NUMBER = 8082
filename = 'data'
commandJsonPath = '../resources/commands.json'

#This class will handles any incoming request from
#the browser 
class dashboard_service_handler(BaseHTTPRequestHandler):

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def encode_resp(self, content):
        return content.format(self.path).encode('utf-8')

    def do_POST(self):
        if self.path=="/add_data":
            content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
            post_data = self.rfile.read(content_length) # <--- Gets the data itself
            self._set_response()
            self.wfile.write(post_data)


        if self.path == '/commands':
            ctype, pdict = parse_header(self.headers['content-type'])

            if ctype == 'multipart/form-data':
                postvars = parse_multipart(self.rfile, pdict)
            elif ctype == 'application/x-www-form-urlencoded':
                length = int(self.headers.getheader('content-length'))
                postvars = parse_qs(self.rfile.read(length), keep_blank_values=1)

            print(postvars)

            # send response to client
            self._set_response()
            self.wfile.write(postvars)

            # add new command to json file
            with open(commandJsonPath) as fjson:    # get json
                dataJson = json.load(fjson)

            dataJson.update({ postvars["question"][0]: postvars["answer"][0] })     # add new element

            with open(commandJsonPath, 'w') as fjson:   # write on file
                json.dump(dataJson, fjson)

            print("command added")
            print("finish processing...")


    #Handler for the GET requests
    def do_GET(self):
        if self.path=="/":
            self.path="/index.html"

        if self.path == '/commands':
            self.send_response(200)
            self.send_header('content-type', 'application/json')
            self.end_headers()
            with open(commandJsonPath) as fjson:    # get json
                dataJson = json.dumps(json.load(fjson))
            self.wfile.write(dataJson)

        try:
            #Check the file extension required and
            #set the right mime type

            sendReply = False
            if self.path.endswith(".html"):
                mimetype='text/html'
                sendReply = True
            if self.path.endswith(".jpg"):
                mimetype='image/jpg'
                sendReply = True
            if self.path.endswith(".gif"):
                mimetype='image/gif'
                sendReply = True
            if self.path.endswith(".js"):
                mimetype='application/javascript'
                sendReply = True
            if self.path.endswith(".css"):
                mimetype='text/css'
                sendReply = True

            if sendReply == True:
                #Open the static file requested and send it
                f = open(curdir + sep + self.path, 'rb')
                self.send_response(200)
                self.send_header('Content-type',mimetype)
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
            return

        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)



    def do_DELETE(self):
        if self.path == '/commands':
            ctype, pdict = parse_header(self.headers['content-type'])

            if ctype == 'multipart/form-data':
                postvars = parse_multipart(self.rfile, pdict)
            elif ctype == 'application/x-www-form-urlencoded':
                length = int(self.headers.getheader('content-length'))
                postvars = parse_qs(self.rfile.read(length), keep_blank_values=1)

            # send response to client
            self._set_response()
            self.wfile.write(postvars)

            # delete command to json file
            with open(commandJsonPath) as fjson:    # get json
                dataJson = json.load(fjson)

            dataJson.pop(postvars["question"][0], None)     # delete element

            with open(commandJsonPath, 'w') as fjson:   # write on file
                json.dump(dataJson, fjson)

            print("command deleted")
            print("finish processing...")


try:
    #Create a web server and define the handler to manage the
    #incoming request
    server = HTTPServer(('', PORT_NUMBER), dashboard_service_handler)
    print ('Started httpserver on port ' + str(PORT_NUMBER))

    #Wait forever for incoming htto requests
    server.serve_forever()


except KeyboardInterrupt:
    print ('^C received, shutting down the web server')
    server.socket.close()