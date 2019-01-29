#!/usr/bin/python
import http.client, base64
from http.server import BaseHTTPRequestHandler,HTTPServer
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import smtplib, ssl
import json
import os
# from textmagic.rest import TextmagicRestClient

PORT_NUMBER = 8080
filename = 'data'

# Face API constants
key = 'd369abc5e70741e5993f9e54e362169f'

mime_octet_stream = 'application/octet-stream'
mime_json = 'application/json'

face_api_url = 'westeurope.api.cognitive.microsoft.com'
face_api_url_extension = "/face/v1.0/detect?%s"
face_api_headers = {'Content-Type': mime_octet_stream, 'Ocp-Apim-Subscription-Key': key }

params = urlencode({
	'returnFaceId': 'true',
	'returnFaceLandmarks': 'false',
	'returnFaceAttributes': 'age,gender,smile,headPose,emotion,exposure'
})

face_sample_image = 'face_sample.jpg'

# Services constants
url_stats = 'http://localhost:8081/compute_stats'
url_dashboard = 'http://localhost:8082/add_data'

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):

	def _set_response(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()

	def encode_resp(self, content):
		return content.format(self.path).encode('utf-8')

	def send_basic_post_request(self, url, content):
		request = Request(url, str.encode(content))
		return urlopen(request).read().decode()

	#Handler for the POST requests
	def do_POST(self):
		if self.path=="/faces":
			# Read post data
			content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
			post_data = self.rfile.read(content_length) # <--- Gets the data itself

			# Send post data to Face API
			conn = http.client.HTTPSConnection(face_api_url)
			conn.request("POST", face_api_url_extension % params, post_data, face_api_headers)
			response = conn.getresponse()
			data = response.read().decode('utf-8')
			conn.close()

			# Print and write received data to the file named 'data'
			print(data)
			with open(filename, 'a+') as file:
				file.write(data + '\n')

			# Send data through statistics then dashboard services
			basic_stats = self.send_basic_post_request(url_stats, data)
			self.send_basic_post_request(url_dashboard, basic_stats)

			# Send response
			self.send_response(200)
			self.send_header('Content-type', 'application/json')
			self.end_headers()

	#Handler for the GET requests
	def do_GET(self):
		if self.path=="/camera_alarm":
			self.sendAlarm()
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			return

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

	def sendAlarm(self):
		SSL_PORT = 465
		SMTP_GMAIL_SERVER = "smtp.gmail.com"

		GMAIL_ACCOUNT = "ocs.frameplus@gmail.com"
		GMAIL_PASSWORD = "frameplus1819"

		sender_email = GMAIL_ACCOUNT
		receiver_email = GMAIL_ACCOUNT
		subject = "Frameplus Camera Alert"
		text = "The camera is obstructed!"
		message = 'Subject: {}\n\n{}'.format(subject, text)

		# Create a secure SSL context
		context = ssl.create_default_context()

		with smtplib.SMTP_SSL(SMTP_GMAIL_SERVER, SSL_PORT, context=context) as smtp_server:
			smtp_server.login(GMAIL_ACCOUNT, GMAIL_PASSWORD)
			smtp_server.sendmail(sender_email, receiver_email, message)

# Execution starts here
try:
	# Create a web server and define the handler to manage the
	# incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print ('Started httpserver on port ' + str(PORT_NUMBER))

	# Wait forever for incoming http requests
	server.serve_forever()


except KeyboardInterrupt:
	print ('^C received, shutting down the web server')
	server.socket.close()
