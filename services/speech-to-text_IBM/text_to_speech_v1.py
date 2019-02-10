# coding=utf-8
from __future__ import print_function
from os.path import join, dirname
from watson_developer_cloud import TextToSpeechV1
from playsound import playsound
from threading import Thread

# If service instance provides API key authentication
service = TextToSpeechV1(
    url='https://gateway-lon.watsonplatform.net/text-to-speech/api',
    iam_apikey='GEvciTdhYRXXAHnXE2HiR9RLADcbgiC2Eq61-hn0VOwe')
#iam_apikey='2rmmSxBMRZAQ2hU1U8wOq0nSw5_DhCi8rRPLo426U2ER')   #CHANGER A CETTE CLE


audio_created = './resources/text_to_speech.wav'


def text_to_speech(text_to_read):
    with open(join(dirname(__file__), audio_created), 'wb') as audio_file:
        print("waiting for response...")
        response = service.synthesize(text_to_read, accept='audio/wav', voice="en-US_AllisonVoice").get_result()
        audio_file.write(response.content)

        # Create and run the thread to play the audio in the background (non-blocking way)
        thread = Thread(target = play_audio)
        thread.start()


def play_audio():
    playsound(audio_created)


file = open("./resources/test.txt", "r")
txt = file.read()
print(txt)
text_to_speech(txt)
print("after audio")