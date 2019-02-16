import numpy as np
import cv2
import time
import paho.mqtt.client as mqtt

try:
	from urllib.parse import urlparse
except ImportError:
	from urlparse import urlparse
from urllib2 import urlopen
import httplib
import sys

mosquitto_mqtt_broker_ip = 'localhost'
mosquitto_mqtt_broker_port = '1883'

mosquitto_mqtt_broker_url = mosquitto_mqtt_broker_ip + ':' + mosquitto_mqtt_broker_port
topic = 'sensors/camera'

print('Mosquitto MQTT Broker url: ' + mosquitto_mqtt_broker_url)

client = mqtt.Client()
client.connect(mosquitto_mqtt_broker_ip, int(mosquitto_mqtt_broker_port), 60)

# multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades
faceCascade = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)
cap.set(3,640) # set Width
cap.set(4,480) # set Height


## welcome audio
#isFirstDetection = False
#isWelcomePlayed = False
#welcome_audio = "./audio/resources/welcome.wav"

print("Detecting...")
while True:
	ret, img = cap.read()
	#img = cv2.flip(img, -1)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	faces = faceCascade.detectMultiScale(
		gray,
		scaleFactor=1.2,
		minNeighbors=5,
		minSize=(20, 20)
	)

	for (x,y,w,h) in faces:
		cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
		roi_gray = gray[y:y+h, x:x+w]
		roi_color = img[y:y+h, x:x+w]

	if len(faces) > 0:
		print ('Detecting ' + str(len(faces)) + ' faces!')
		cv2.imwrite('images/face.jpg', gray, [int(cv2.IMWRITE_JPEG_QUALITY)])
		local_data = open('images/face.jpg', 'rb').read()
		client.publish(topic, payload=local_data, qos=0, retain=False)


		# if not isFirstDetection:
		# 	print("First detection...")
		# 	isFirstDetection = True
		# 	isWelcomePlayed = audio.play_audio(welcome_audio)
		# 	#print("Was audio played: " + isWelcomePlayed)
		#
		# # if the face was detected for the first time but for some reason the welcome audio was not played then try to play it again
		# elif isFirstDetection and not isWelcomePlayed:
		# 	isWelcomePlayed = audio.play_audio(welcome_audio)
		#

		time.sleep(3)
	# else:
	# 	isFirstDetection = False
	#	# TODO: peut-etre il manque un compteur pour ne pas remettre a False tout suite quand il n'y a pas de detection en cas de erreur de detection


	#cv2.imshow('video',img)
	k = cv2.waitKey(30) & 0xff
	if k == 27: # press 'ESC' to quit
		break

cap.release()
cv2.destroyAllWindows()
