from http.server import BaseHTTPRequestHandler
from urllib.parse import urlencode
from urllib.request import Request, urlopen

PORT_NUMBER = 8080

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

    # Handler for the POST requests
    def do_POST(self):
        if self.path == '/audioFile':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            # speech to ext job ----------------
            response = speech.mainSpeechToText(post_data)  # (post_data)
            if response == None:
                response = "I don't understand"
            fileName = text.text_to_speech(response)

            #send file to raspberry pi
            with open(fileName, 'rb') as data:
                requests.post('http://176.143.207.186:2222/play_sound', files = {'file1': data} )

            # Send response
            self._set_response()

    # Handler for the GET requests
    def do_GET(self):
        if self.path=="/api/data/total_faces" or self.path=="/api/data/avg_age" or self.path=="/api/data/parity" or self.path=="/api/data/expressions":
            self._set_response(mime_json)
            self.wfile.write(self.send_basic_get_request(url_stats, self.path))