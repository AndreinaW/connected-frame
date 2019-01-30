import numpy as np
import cv2
import time

try:
	from urllib.parse import urlparse
except ImportError:
	from urlparse import urlparse
from urllib2 import urlopen
import httplib
import sys

mime_octet_stream = 'application/octet-stream'
mime_json = 'application/json'

app_ip = 'localhost'
app_port = '8080'

if len(sys.argv) == 3:
	app_ip = sys.argv[1]
	app_port = sys.argv[2]

app_url = app_ip + ':' + app_port
app_url_extension = "/faces"
app_api_headers = {'Content-Type': mime_octet_stream }

print('Server url: ' + app_url)

# multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades
faceCascade = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)
cap.set(3,640) # set Width
cap.set(4,480) # set Height

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
		conn = httplib.HTTPConnection(app_url)
		conn.request("POST", app_url_extension, local_data)
		time.sleep(3)

	#cv2.imshow('video',img)
	k = cv2.waitKey(30) & 0xff
	if k == 27: # press 'ESC' to quit
		break

cap.release()
cv2.destroyAllWindows()
