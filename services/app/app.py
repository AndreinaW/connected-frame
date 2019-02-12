#!/usr/bin/python
import smtplib
import ssl
import json
import os
import sys
import requests

# os.chdir('/Users/asia/Desktop/connected-frame/speech')
# print(sys.path)
#import speech
#path ='/Users/asia/Desktop/connected-frame/'
# file=open('speech'.join(path,'speech'))
# sys.path.append('/Users/asia/Desktop/connected-frame/speech-to-text_IBM')
#from .. import speech
# sys.path.append('/Users/asia/Desktop/connected-frame/speech-to-text_IBM')
#sys.path.insert(0, '/Users/asia/Desktop/connected-frame/services')


# http
import http.client
from http.server import HTTPServer
import Http_App_Server as Http_App_Server
from urllib.parse import urlencode



# mqtt
import paho.mqtt.subscribe as subscribe
import multiprocessing

#Text to speech
import speech_to_text as speech
import text_to_speech as text

# Face API constants
key = 'd369abc5e70741e5993f9e54e362169f'

mime_octet_stream = 'application/octet-stream'

face_api_url = 'westeurope.api.cognitive.microsoft.com'
face_api_url_extension = '/face/v1.0/detect?%s'
face_api_headers = {'Content-Type': mime_octet_stream,
    'Ocp-Apim-Subscription-Key': key}
raspberry_pi_headers = {'Content-Type': mime_octet_stream}

params = urlencode({
                   'returnFaceId': 'true',
                   'returnFaceLandmarks': 'false',
                   'returnFaceAttributes': 'age,gender,smile,headPose,emotion,exposure'
                   })

resources_file = 'resources/'
filename = resources_file + 'data'
face_sample_image = resources_file + 'face_sample.jpg'

# MQTT Constants
raspi_mqtt_broker_ip = ''
raspi_mqtt_broker_port = 1883
topics = {'sensors/camera', 'sensors/light', 'audio_register'}

# Services constants
url_stats = 'http://localhost:8081'
url_stats_post_extension = '/compute_stats'
url_dashboard = 'http://localhost:8082/add_data'

# This class will handles any incoming request from
# the browser
class myHandler(BaseHTTPRequestHandler):

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def encode_resp(self, content):
        return content.format(self.path).encode('utf-8')

    # Handler for the POST requests
    def do_POST(self):
        
        if self.path == '/faces':
            # Read post data
            # <--- Gets the size of data
            content_length = int(self.headers['Content-Length'])
            # <--- Gets the data itself
            post_data = self.rfile.read(content_length)

            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

    # Handler for the GET requests

    def do_GET(self):
        if self.path == '/camera_alarm':
            send_alarm()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            return

        try:
            # Check the file extension required and
            # set the right mime type

            sendReply = False
            if self.path.endswith('.html'):
                mimetype = 'text/html'
                sendReply = True
            if self.path.endswith('.jpg'):
                mimetype = 'image/jpg'
                sendReply = True
            if self.path.endswith('.gif'):
                mimetype = 'image/gif'
                sendReply = True
            if self.path.endswith('.js'):
                mimetype = 'application/javascript'
                sendReply = True
            if self.path.endswith('.css'):
                mimetype = 'text/css'
                sendReply = True

            if sendReply == True:
                # Open the static file requested and send it
                f = open(curdir + sep + self.path, 'rb')
                self.send_response(200)
                self.send_header('Content-type', mimetype)
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
            return
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)


def send_basic_post_request(url, content):
    request = Request(url, str.encode(content))
    return urlopen(request).read().decode()

def speech_text(audio_file):
        # speech to ext job ----------------
        response = speech.mainSpeechToText(audio_file)  # (post_data)
        if response == None:
            response = "I don't understand"
            fileName = text.text_to_speech(response)
            
            # Print and write file's name
            print(fileName)
            
            #send file to raspberry pi
            with open(fileName, 'rb') as data:
                requests.post('http://176.143.207.186:2222/play_sound', files = {'file1': data} )
            
            # Send response
            self._set_response()



def face_api(data):
    # Send post data to Face API
    conn = http.client.HTTPSConnection(face_api_url)
    conn.request('POST', face_api_url_extension %
                    params, data, face_api_headers)
    response = conn.getresponse()
    data = response.read().decode('utf-8')
    conn.close()

    # Print and write received data to the file named 'data'
    print(data)
    with open(filename, 'a+') as file:
        file.write(data + '\n')

    # Send data through statistics then dashboard services
    send_basic_post_request(url_stats, data)


def send_alarm():
        SSL_PORT = 465
        SMTP_GMAIL_SERVER = 'smtp.gmail.com'

        GMAIL_ACCOUNT = 'ocs.frameplus@gmail.com'
        GMAIL_PASSWORD = 'frameplus1819'

        sender_email = GMAIL_ACCOUNT
        receiver_email = GMAIL_ACCOUNT
        subject = 'Frameplus Camera Alert'
        text = 'The camera is obstructed!'
        message = 'Subject: {}\n\n{}'.format(subject, text)

        # Create a secure SSL context
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(SMTP_GMAIL_SERVER, SSL_PORT, context=context) as smtp_server:
            smtp_server.login(GMAIL_ACCOUNT, GMAIL_PASSWORD)
            smtp_server.sendmail(sender_email, receiver_email, message)


def on_message_received(client, userdata, message):
    if message.topic == topics[0]:
        print('Photo published on ' + message.topic)
        face_api(message.payload)
    elif message.topic == topics[1]:
        print('%s %s' % (message.topic, message.payload))
        send_alarm()
    elif message.topic == topics[2]:
        print('Speech to text - text to speech ' + message.topic)
        speech_text(message.payload)


if len(sys.argv) > 1:
    raspi_mqtt_broker_ip = sys.argv[1]
    if len(sys.argv) > 2:
        raspi_mqtt_broker_port = int(sys.argv[2])
else:
    sys.exit('Usage: python <program_name>.py [Required: mqtt_broker_ip] [Optional: mqtt_broker_port (Default = 1883)]')

client = mqtt.Client('Frameplus Client')
client.on_message = on_message_received
client.connect(raspi_mqtt_broker_ip, port=raspi_mqtt_broker_port)
print('Subscribing to %s:%i on topics: ' % (raspi_mqtt_broker_ip, raspi_mqtt_broker_port))
print(*topics, sep=', ')
client.subscribe([(topics[0], 0), (topics[1], 0), (topics[2], 0)])

# Execution starts here
try:
    client.loop_start()

    # Create a web server and define the handler to manage the
    # incoming request
    server = HTTPServer(('', PORT_NUMBER), Http_App_Server)
    print('Started httpserver on port ' + str(PORT_NUMBER))

    # Wait forever for incoming http requests
    server.serve_forever()


except KeyboardInterrupt:
    print('^C received, shutting down the web server')
    server.socket.close()
    client.loop_stop()
