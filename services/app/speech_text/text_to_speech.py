# coding=utf-8
from __future__ import print_function
from os.path import join, dirname
from watson_developer_cloud import TextToSpeechV1

# If service instance provides API key authentication
service = TextToSpeechV1(
    url='https://gateway-lon.watsonplatform.net/text-to-speech/api',
    iam_apikey='GEvciTdhYRXXAHnXE2HiR9RLADcbgiC2Eq61-hn0VOwe')

audio_created = './recordings/text_to_speech.wav'

def text_to_speech(text):
    with open(join(dirname(__file__), audio_created), 'wb') as audio_file:
        print("waiting for response...")
        response = service.synthesize(text, accept='audio/wav', voice="en-US_AllisonVoice").get_result()
        audio_file.write(response.content)
    return audio_created
