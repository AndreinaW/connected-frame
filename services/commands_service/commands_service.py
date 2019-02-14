#!/usr/bin/python
# -*- coding: utf-8 -*-

from http.server import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import json
import re
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
        
            with open(commandJsonPath) as fjson:    # get json
                dataJson = json.load(fjson)

            key_dict = postvars[b'question'][0].decode("utf-8")
            value_dict = postvars[b'answer'][0].decode("utf-8")

            #add question/response to dict
            dataJson[key_dict] = value_dict
                
            with open(commandJsonPath, 'w') as fjson:   # write on file
                    json.dump(dataJson, fjson)

            # send response to client
            self._set_response()
            self.wfile.write(dataRead)
            print("command added")
            print("finish processing...")



        if self.path == '/commands/match':
            content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
            post_data = self.rfile.read(content_length).decode("utf-8") # <--- Gets the data itself

            # check if there is a match
            listWordsSpeech = self.retriveWordsSpeech(post_data)
            listKeywords = self.retriveKeyWordsFromFile()
            match = self.matchWordsWithKeywords(listWordsSpeech, listKeywords)

            self._set_response()
            self.wfile.write(str.encode(match))
            print("command matched")
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

            # send response to client
            self._set_response()
            self.wfile.write(dataRead)

            # delete command to json file
            with open(commandJsonPath) as fjson:    # get json
                dataJson = json.load(fjson)
            
            key_dict = postvars[b'question'][0].decode("utf-8")
            print("key_dict  " + str(key_dict))

            del dataJson[key_dict]

            with open(commandJsonPath, 'w') as fjson:   # write on file
                json.dump(dataJson, fjson)

            print("command deleted")
            print("finish processing...")



    # retrive words from user's speech -> in form of list of words
    def retriveWordsSpeech(self, textRecognized):
        keyWords = re.findall("[a-z]+", textRecognized)
        # res = []
        # for el in keyWords:
        #     res.append(el[1:-1])
        # res = res[4:]
        print("Retrive words from user's speech : " )
        print(keyWords)
        return keyWords

    #retrive the keywords(questions) from the file containing dictionary of form question:response
    def retriveKeyWordsFromFile(self):
        with open(commandJsonPath) as fjson:    # get list of keywords and their response
            listKeywordResponse = json.load(fjson)
            listKeywordResponse = {k.lower():v for k,v in listKeywordResponse.items()}
        return listKeywordResponse

    # match if user's speech corresponds to any keyword in dictionary
    def matchWordsWithKeywords(self, listWords, listKeywordResponse):
        for w in listWords:
            word = w.lower()
            if word in listKeywordResponse:
                print("Found matching for sentence : " + word)
                print("The response from speech to text : " + listKeywordResponse[word])
                return listKeywordResponse[word]
        print("Matching not found ! ")
        return "None"


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
