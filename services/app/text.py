# coding=utf-8
from __future__ import print_function
import json
from os.path import join, dirname
from watson_developer_cloud import TextToSpeechV1
from watson_developer_cloud.websocket import SynthesizeCallback

# If service instance provides API key authentication
service = TextToSpeechV1(
     ## url is optional, and defaults to the URL below. Use the correct URL for your region.
                         url='https://gateway-lon.watsonplatform.net/text-to-speech/api',
    

                         iam_apikey='nvaRIC76wDzVic9cQ--abLTni5y5d8Pl5ZuhTU5t9LHf')   #CHANGER A CETTE CLE


# Synthesize using websocket. Note: The service accepts one request per connection
file_path = join(dirname(__file__), "./resources/text_to_speech.wav")

class MySynthesizeCallback(SynthesizeCallback):
    def __init__(self):
        SynthesizeCallback.__init__(self)
        self.fd = open(file_path, 'wb')

    def on_connected(self):
        print('Connection was successful')

    def on_error(self, error):
        print('Error received: {}'.format(error))

    def on_content_type(self, content_type):
        print('Content type: {}'.format(content_type))

    def on_timing_information(self, timing_information):
        print(timing_information)

    def on_audio_stream(self, audio_stream):
        self.fd.write(audio_stream)

    def on_close(self):
        self.fd.close()
        print('Done synthesizing. Closing the connection')


def mainTextToSpeech(txt):
    #file = open("./resources/" + fileTxt, "r")
    #txt = file.read()
    print("text to speech : " + txt)
    my_callback = MySynthesizeCallback()
    res = service.synthesize_using_websocket(txt,
                                       my_callback,
                                       accept='audio/wav',
                                       voice='en-US_AllisonVoice'
                                       )
    return my_callback.fd

#def mainTextToSpeech(txt):
#    with open('hello_world.wav', 'wb') as audio_file:
#        audio_file.write(
#                         service.synthesize(
#                                                   txt,
#                                                   'audio/wav',
#                                                   'en-US_AllisonVoice'
#                                                   ).get_result().content)

#mainTextToSpeech("Never say never again and again ")
