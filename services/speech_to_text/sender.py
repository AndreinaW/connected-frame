#!/usr/bin/python
import http.client, base64
from http.server import BaseHTTPRequestHandler,HTTPServer
from urllib.parse import urlencode
from urllib.request import Request, urlopen

mime_octet_stream = 'application/octet-stream'
mime_json = 'application/json'

app_url = 'localhost:8080'
app_url_extension = "/audioFile"
face_api_headers = {'Content-Type': mime_octet_stream }

speech_sample_wav = 'speech.wav'

local_data = open(speech_sample_wav, 'rb').read()
conn = http.client.HTTPConnection(app_url)
conn.request("POST", app_url_extension, local_data)
