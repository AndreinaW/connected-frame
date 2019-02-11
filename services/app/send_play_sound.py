#!/usr/bin/python
import http.client, base64
from http.server import BaseHTTPRequestHandler,HTTPServer
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import requests

mime_octet_stream = 'application/octet-stream'
mime_json = 'application/json'

app_url = 'http://176.143.207.186:2222'
app_url_extension = "/play_sound"
face_api_headers = {'Content-Type': mime_octet_stream }

face_sample_image = 'test.wav'

local_data = open(face_sample_image, 'rb')
#conn = http.client.HTTPConnection(app_url)
#conn.request("POST", app_url_extension, local_data)




#r = requests.post("http://bugs.python.org", data={'number': 12524, 'type': 'issue', 'action': 'show'})

with open("test.wav", 'rb') as data:
    requests.post('http://176.143.207.186:2222/play_sound', files = {'file1': data} )
