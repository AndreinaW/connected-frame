#!/usr/bin/python
import smtplib
import ssl
import json
import os
import sys
import requests

# http
import http.client
from http.server import HTTPServer
from Http_App_Server import Http_App_Server
from urllib.parse import urlencode

# mqtt
import paho.mqtt.subscribe as subscribe
import paho.mqtt.client as mqtt
import multiprocessing

# Speech to Text - Text to speech
from watson_developer_cloud import TextToSpeechV1, SpeechToTextV1

PORT_NUMBER = 8080

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
topics = ['sensors/camera', 'sensors/light', 'audio/register']

# Services constants
url_stats = 'http://localhost:8081'
url_stats_post_extension = '/compute_stats'
raspberry_pi_url = ''
raspberry_pi_url_extension = '/audioResponse'

url_match_commands = 'http://localhost:8083/commands/match'
audio_created = './recordings/text_to_speech.wav'
url_node_red = 'http://192.168.43.108:1880/play_sound'

serviceSpeechToText = SpeechToTextV1(
    url='https://gateway-lon.watsonplatform.net/speech-to-text/api',
    iam_apikey='57ZvOyql78xGGdNlwd3BBHlio9wm5_ldItfG1kpFw3sa')

serviceTextToSpeech = TextToSpeechV1(
    url='https://gateway-lon.watsonplatform.net/text-to-speech/api',
    iam_apikey='GEvciTdhYRXXAHnXE2HiR9RLADcbgiC2Eq61-hn0VOwe')



def speech_text(audio_file):
    # speech to text
    recognized = serviceSpeechToText.recognize(audio=audio_file,
                                    content_type='application/octet-stream',
                                    timestamps=True,
                                    word_confidence=True).get_result()
    textRecognized = json.dumps(recognized)

    print("recognized... now matching ")

    # match words
    response = requests.post(url_match_commands, textRecognized)

    print("matched... now waiting response ")

    if response.text == "None":
        print("I don't understand")
    else:
        print("sending text to speech...")
        print(response.text)
        with open(audio_created, 'wb') as audio_file:
            res = serviceTextToSpeech.synthesize(response.text, accept='audio/wav', voice="en-US_AllisonVoice").get_result()
            audio_file.write(res.content)

        # send file to raspberry pi
        print("send back to arduino...")
        with open(audio_created, 'rb') as data:
            requests.post(url_node_red, files = {'file1': data} )


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
