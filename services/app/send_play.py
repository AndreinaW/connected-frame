
#!/usr/bin/python
import http.client, base64
from http.server import BaseHTTPRequestHandler,HTTPServer
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import requests


mime_octet_stream = 'application/octet-stream'
mime_json = 'application/json'

app_url = 'localhost:8080'
app_url_extension = "/audioFile"
headers = {'content-type': 'audio/wav'}

sample_audio = 'test.wav'

face_api_headers = {'Content-Type': mime_octet_stream }


local_data = open(sample_audio, 'rb').read()
conn = http.client.HTTPConnection(app_url)
#resp = conn.request("POST", app_url_extension, local_data, headers)
resp = conn.request("POST", app_url_extension, local_data, face_api_headers)
print('Yay, got Wit.ai response: ' + str(resp))



#fobj = open(sample_audio, 'rb')
#conn.request("POST", app_url_extension, {'speech.wav', fobj})

#url = app_url + app_url_extension
#r = requests.post(url, data=local_data, headers=headers)

#print(r)
#print(r.text)
