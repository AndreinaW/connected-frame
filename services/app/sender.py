#!/usr/bin/python
import http.client, base64
from http.server import BaseHTTPRequestHandler,HTTPServer
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json

# Face API constants
key = 'd369abc5e70741e5993f9e54e362169f'

mime_octet_stream = 'application/octet-stream'
mime_json = 'application/json'

app_url = 'localhost:8080'
app_url_extension = "/faces"
face_api_headers = {'Content-Type': mime_octet_stream }

face_sample_image = 'face_sample.jpg'

local_data = open(face_sample_image, 'rb').read()
conn = http.client.HTTPConnection(app_url)
conn.request("POST", app_url_extension, local_data)

