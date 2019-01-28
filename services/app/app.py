#!/usr/bin/python
from http.server import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import smtplib, ssl
# from textmagic.rest import TextmagicRestClient

PORT_NUMBER = 8080
filename = 'data'

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):

	def _set_response(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()

	def encode_resp(self, content):
		return content.format(self.path).encode('utf-8')

	#Handler for the POST requests
	def do_POST(self):
		if self.path=="/faces":
			content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
			post_data = self.rfile.read(content_length) # <--- Gets the data itself
			self._set_response()
			self.wfile.write(post_data)
			
			with open(filename, 'a+') as file:
				file.write(post_data.decode('utf-8') + '\n')

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
