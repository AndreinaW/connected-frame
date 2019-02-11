#!/usr/bin/python
import smtplib
import ssl
import sys

# http
import http.client
from urllib.parse import urlencode
from urllib.request import Request, urlopen

# mqtt
import paho.mqtt.subscribe as subscribe
import paho.mqtt.client as mqtt


# Services constants
url_stats = 'stats:8081/compute_stats'
url_dashboard = 'dashboard:8082/add_data'

url_stats = 'http://localhost:8081'
url_stats_post_extension = '/compute_stats'
url_dashboard = 'http://localhost:8082/add_data'


# Face API constants
key = 'd369abc5e70741e5993f9e54e362169f'

mime_octet_stream = 'application/octet-stream'
mime_json = 'application/json'

face_api_url = 'westeurope.api.cognitive.microsoft.com'
face_api_url_extension = '/face/v1.0/detect?%s'
face_api_headers = {'Content-Type': mime_octet_stream,
                    'Ocp-Apim-Subscription-Key': key}

params = urlencode({
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender,smile,headPose,emotion,exposure'
})

filename = 'data'
face_sample_image = 'face_sample.jpg'


# MQTT Constants
raspi_mqtt_broker_ip = ''
raspi_mqtt_broker_port = 1883
topics = ['sensors/camera', 'sensors/light']


if len(sys.argv) > 1:
    raspi_mqtt_broker_ip = sys.argv[1]
    if len(sys.argv) > 2:
        raspi_mqtt_broker_port = int(sys.argv[2])
else:
    sys.exit('Usage: python <program_name>.py [Required: mqtt_broker_ip] [Optional: mqtt_broker_port (Default = 1883)]')


def send_basic_post_request(url, content):
    request = Request(url, str.encode(content))
    return urlopen(request).read().decode()


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
    basic_stats = send_basic_post_request(url_stats, data)
    send_basic_post_request(url_dashboard, basic_stats)


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


client = mqtt.Client('Frameplus Client')
client.on_message = on_message_received
client.connect(raspi_mqtt_broker_ip, port=raspi_mqtt_broker_port)
print('Subscribing to %s:%i on topics: ' % (raspi_mqtt_broker_ip, raspi_mqtt_broker_port))
print(*topics, sep=', ')
client.subscribe([(topics[0], 0), (topics[1], 0)])


try:
    client.loop_forever()

except KeyboardInterrupt:
    print('^C received, shutting down the mqtt subscribe script')
    client.disconnect()

