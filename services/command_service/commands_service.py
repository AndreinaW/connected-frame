#!/usr/bin/python
from http.server import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import json
from cgi import parse_header, parse_multipart, parse_qs


PORT_NUMBER = 8083
filename = 'data'
commandJsonPath = './commands.json'

#This class will handles any incoming request from
#the browser 
class commands_service_handler(BaseHTTPRequestHandler):

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def encode_resp(self, content):
        return content.format(self.path).encode('utf-8')

    def do_POST(self):
        if self.path == '/commands':
            ctype, pdict = parse_header(self.headers['content-type'])

            if ctype == 'multipart/form-data':
                postvars = parse_multipart(self.rfile, pdict)
            elif ctype == 'application/x-www-form-urlencoded':
                length = int(self.headers['content-length'])
                dataRead = self.rfile.read(length)
                postvars = parse_qs(dataRead, keep_blank_values=1)

            print(postvars)

            # send response to client
            self._set_response()
            self.wfile.write(dataRead)

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
            self.path = commandJsonPath

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
            if self.path.endswith(".json"):
                mimetype='aplication/json'
                sendReply = True

            if sendReply == True:
                #Open the static file requested and send it
                f = open(curdir + sep + self.path, 'rb')
                self.send_response(200)
                self.send_header('content-type',mimetype)
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
            return

        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

        print("finish processing...")



    def do_DELETE(self):
        if self.path == '/commands':
            ctype, pdict = parse_header(self.headers['content-type'])

            if ctype == 'multipart/form-data':
                postvars = parse_multipart(self.rfile, pdict)
            elif ctype == 'application/x-www-form-urlencoded':
                length = int(self.headers['content-length'])
                dataRead = self.rfile.read(length)
                postvars = parse_qs(dataRead, keep_blank_values=1)

            print(postvars)

            # send response to client
            self._set_response()
            self.wfile.write(dataRead)

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
    server = HTTPServer(('', PORT_NUMBER), commands_service_handler)
    print ('Started httpserver on port ' + str(PORT_NUMBER))

    #Wait forever for incoming htto requests
    server.serve_forever()


except KeyboardInterrupt:
    print ('^C received, shutting down the web server')
    server.socket.close()