from __future__ import print_function
import json
import re
from os.path import join, dirname
from watson_developer_cloud import SpeechToTextV1
from watson_developer_cloud.websocket import RecognizeCallback, AudioSource
import threading

#importing dictionary of form question:response
from Dict import dict



# If service instance provides API key authentication
service = SpeechToTextV1(
#     ## url is optional, and defaults to the URL below. Use the correct URL for your region.
url='https://gateway-lon.watsonplatform.net/speech-to-text/api',
iam_apikey='57ZvOyql78xGGdNlwd3BBHlio9wm5_ldItfG1kpFw3sa')



def recognition(path):
    audio_file = open(join(dirname(__file__), path),
                      'rb')
    recognized = service.recognize(
                                  audio=audio_file,
                                  content_type='audio/wav',
                                  timestamps=True,
                                  word_confidence=True)
    textRecognized = json.dumps(recognized.get_result())
    #print(textRecognized)
    return textRecognized

#retrive words from user's speech -> in form of list of words
def retriveWordsSpeech(textRecognized):
    keyWords = re.findall('"[a-z]+"', textRecognized[50:])
    res = []
    for el in keyWords:
        if ("confidence" in el):
            break
        res.append(el[1:-1])
    print("Retrive words from user's speech : " )
    print(res)
    return res


#retrive the keywords(questions) from the file containing all questions avaliable
def retriveKeyWordsFromFile(filePath):
    keyWords = open(filePath,'r')
    questions = []
    questions = keyWords.readlines()
    res = []
    for question in questions:
        res.append(question.strip())
    return res

#retrive the keywords(questions) from the file containing dictionary of form question:response
def retriveKeyWordsFromFile():
    res = []
    for x, y in dict.items():
        res.append(x)
    #print(res)
    return res


#match if user's speech correspends to any keyword in dictionary
def matchWordsWithKeywords(listWords, listKeywords):
    for question in listKeywords:
        questionLowCase = question.lower()
        #print(questionLowCase)
        wordsInQuestion = question.split(" ")
        size = len(wordsInQuestion)
        compt = 0
        for word in listWords:
            #print("word : " + word)
            #print("questionLowCase : " + questionLowCase)
            if questionLowCase not in word:
                #print("not in question")
                compt = 0
            else:
                compt+=1
            if compt == size:
                print("Found matching for sentence : " + questionLowCase)
                print("The response : " + dict[questionLowCase])
                return dict[questionLowCase]
        compt = 0
    print("Matching not found ! ")
    return None





# Example using websockets
class MyRecognizeCallback(RecognizeCallback):
    def __init__(self):
        RecognizeCallback.__init__(self)

    def on_transcription(self, transcript):
        print(transcript)

    def on_connected(self):
        print('Connection was successful')

    def on_error(self, error):
        print('Error received: {}'.format(error))

    def on_inactivity_timeout(self, error):
        print('Inactivity timeout: {}'.format(error))

    def on_listening(self):
        print('Service is listening')

    def on_hypothesis(self, hypothesis):
        print(hypothesis)

    def on_data(self, data):
        print(data)


def  mainSpeechToText(file):
    textRecognized = recognition('./resources/test.wav')
    listWordsSpeech = retriveWordsSpeech(textRecognized)
    #listKeywords = retriveKeyWords('./key_words_questions.txt')
    listKeywords = retriveKeyWordsFromFile()
    print(listKeywords)
    ifMatched = matchWordsWithKeywords(listWordsSpeech, listKeywords)
    return ifMatched












