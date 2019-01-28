#!/usr/bin/python
from http.server import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep

PORT_NUMBER = 8081
filename = 'data'

#This class will handles any incoming request from
#the browser 
class statistics_service_handler(BaseHTTPRequestHandler):

	def _set_response(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()

	def encode_resp(self, content):
		return content.format(self.path).encode('utf-8')

	def do_POST(self):
		if self.path=="/compute_stats":
			content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
			post_data = self.rfile.read(content_length) # <--- Gets the data itself
			self._set_response()
			self.wfile.write(post_data)
			
			with open(filename, 'a+') as file:
				file.write(post_data.decode('utf-8') + '\n')

try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), statistics_service_handler)
	print ('Started httpserver on port ' + str(PORT_NUMBER))
	
	#Wait forever for incoming htto requests
	server.serve_forever()


except KeyboardInterrupt:
	print ('^C received, shutting down the web server')
	server.socket.close()

