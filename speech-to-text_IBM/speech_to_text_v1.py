from __future__ import print_function
import json
import re
from os.path import join, dirname
from watson_developer_cloud import SpeechToTextV1
from watson_developer_cloud.websocket import RecognizeCallback, AudioSource
import threading

# If service instance provides API key authentication
service = SpeechToTextV1(
#     ## url is optional, and defaults to the URL below. Use the correct URL for your region.
url='https://gateway-lon.watsonplatform.net/speech-to-text/api',


iam_apikey='2rmmSxBMRZAQ2hU1U8wOq0nSw5_DhCi8rRPLo426U2ER')   #CHANGER A CETTE CLE



def recognition(path):
    audio_file = open(join(dirname(__file__), path), 'rb')
    recognized = service.recognize(
                                  audio=audio_file,
                                  content_type='audio/wav',
                                  timestamps=True,
                                  word_confidence=True)
    textRecognized = json.dumps(recognized.get_result())
    #print(textRecognized)
    return textRecognized


def retriveWords(textRecognized):
    keyWords = re.findall('"[a-z]+"', textRecognized[50:])
    res = []
    for el in keyWords:
        if ("confidence" in el):
            break
        res.append(el[1:-1])
    print(res)


# Example using websockets
# class MyRecognizeCallback(RecognizeCallback):
#     def __init__(self):
#         RecognizeCallback.__init__(self)
#
#     def on_transcription(self, transcript):
#         print(transcript)
#
#     def on_connected(self):
#         print('Connection was successful')
#
#     def on_error(self, error):
#         print('Error received: {}'.format(error))
#
#     def on_inactivity_timeout(self, error):
#         print('Inactivity timeout: {}'.format(error))
#
#     def on_listening(self):
#         print('Service is listening')
#
#     def on_hypothesis(self, hypothesis):
#         print(hypothesis)
#
#     def on_data(self, data):
#         print(data)




textRecognized = recognition('./resources/speech.wav')
retriveWords(textRecognized)
# Example using threads in a non-blocking way
#mycallback = MyRecognizeCallback()
#audio_file = open(join(dirname(__file__), '../resources/speech.wav'), 'rb')
#audio_source = AudioSource(audio_file)
#recognize_thread = threading.Thread(
#   target=service.recognize_using_websocket,
#   args=(audio_source, "audio/l16; rate=44100", mycallback))
#recognize_thread.start()
