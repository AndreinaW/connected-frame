#!/usr/bin/python
from http.server import BaseHTTPRequestHandler,HTTPServer
from json_handler import JsonHandler
from os import curdir, sep

import json

filename = 'data'

PORT_NUMBER = 8081

#This class will handles any incoming request from
#the browser 
class statistics_service_handler(BaseHTTPRequestHandler):

	def _set_response(self):
		self.send_response(200)
		self.send_header('Content-type', 'application/json')
		self.end_headers()

	def encode_resp(self, content):
		return content.format(self.path).encode('utf-8')

	def set_return_json(self, json_result):
		self.wfile.write(json_result)

	def do_GET(self):
		if self.path=="/api/data/total_faces":
			self._set_response()
			self.wfile.write(JsonHandler(filename).get_data_from_file("totalFaces"))

		elif self.path=="/api/data/avg_age":
			self._set_response()
			self.wfile.write(JsonHandler(filename).get_data_from_file("currentAverageAge"))

		elif self.path=="/api/data/parity":
			self._set_response()
			self.wfile.write(JsonHandler(filename).get_data_from_file("parity"))

		elif self.path=="/api/data/expressions":
			self._set_response()
			self.wfile.write(JsonHandler(filename).get_data_from_file("expressions"))

	def do_POST(self):
		if self.path=="/compute_stats":
			content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
			post_data = self.rfile.read(content_length) # <--- Gets the data itself
			self._set_response()

			JsonHandler(filename).process_data_from_json(post_data)

			self.wfile.write(post_data)

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

