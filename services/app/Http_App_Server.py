#!/usr/bin/python
import smtplib
import ssl
import json
import os
import sys
import requests

# http
import http.client
from urllib.parse import urlencode
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.request import Request, urlopen

mime_json = 'application/json'

url_stats = 'http://localhost:8081'

# Class representing our app server
class Http_App_Server(BaseHTTPRequestHandler):

    def _set_response(self, content_type='text/html'):
        self.send_response(200)
        self.send_header('Content-type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def encode_resp(self, content):
        return content.format(self.path).encode('utf-8')

    def send_basic_post_request(url, content):
        request = Request(url, str.encode(content))
        return urlopen(request).read().decode()

    def send_basic_get_request(self, url, extra_path):
        request = Request(url + extra_path)
        return urlopen(url + extra_path).read()

    # Handler for the GET requests
    def do_GET(self):
        if self.path=="/api/data/total_faces" or self.path=="/api/data/avg_age" or self.path=="/api/data/parity" or self.path=="/api/data/expressions":
            self._set_response(mime_json)
            self.wfile.write(self.send_basic_get_request(url_stats, self.path))