#!/usr/bin/python
from http.server import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
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

	def do_POST(self):
		if self.path=="/faces":
			content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
			post_data = self.rfile.read(content_length) # <--- Gets the data itself
			self._set_response()
			self.wfile.write(post_data)
			
			with open(filename, 'a+') as file:
				file.write(post_data.decode('utf-8') + '\n')

	"""def sendAlarm(self):
		username = "johndoe64"
		token = "3wJAzbuo9n3zOcTYAz6h0yX2BKozVf"
		client = TextmagicRestClient(username, token)
		message = client.messages.create(phones="+33648368143", text="The camera is getting into troubles")"""

	#Handler for the GET requests
	def do_GET(self):
		if self.path=="/":
			self.path="/index.html"
		if self.path=="/camera_alarm":
			self.sendAlarm()

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

try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print ('Started httpserver on port ' + str(PORT_NUMBER))
	
	#Wait forever for incoming htto requests
	server.serve_forever()


except KeyboardInterrupt:
	print ('^C received, shutting down the web server')
	server.socket.close()

