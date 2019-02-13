# coding=utf-8
import subprocess
import snowboydecoder
import sys
import signal
import time
import paho.mqtt.client as mqtt

#************* mqtt *************
mosquitto_mqtt_broker_ip = 'localhost'
mosquitto_mqtt_broker_port = '1883'

mosquitto_mqtt_broker_url = mosquitto_mqtt_broker_ip + ':' + mosquitto_mqtt_broker_port
topic = 'audio_registered'


print('Mosquitto MQTT Broker url: ' + mosquitto_mqtt_broker_url)

client = mqtt.Client()
client.connect(mosquitto_mqtt_broker_ip, int(mosquitto_mqtt_broker_port), 60)

#************* mqtt *************

interrupted = False
play_is_success = True
hotword_model = "./resources/ConnectedFrame.pmdl"

duration = "5"
adresse_mac_speakers = "78:44:05:DA:56:65"
welcome_audio = "./resources/welcome.wav"
beep_audio = "./resources/ding.wav"
#audio_recorded = "./recordings/audio_recorded.wav"


#def record_audio():
    # with .call if there is an error while executing the command; It won't make an exception and stop executing the .py
#    subprocess.call(['arecord', '-f', 'cd', '-d', duration, audio_recorded])


def play_audio(audio_path):
    # with .call if there is an error while executing the command; It won't make an exception and stop executing the .py
    global play_is_success
    i = 0;
    result =  1
    while result and i < 3:
        i = i + 1
        result = subprocess.call(['aplay', '-D', 'bluealsa:DEV=' + adresse_mac_speakers, audio_path])
        if result != 0:
            time.sleep(3)
            play_is_success = False
            print("waiting to play audio...")
        else:
            play_is_success = True


def play_welcome():
    play_audio(welcome_audio)

def play_beep():
    play_audio(beep_audio)


def audio_rec_callback(fname):
    print("beep FINISH recording...")
    global play_is_success
    play_beep()
    play_audio(fname)   # todo: erase this


    if play_is_success:
        print("publish to topic")
        #************* mqtt *************
        #local_data = open(audio_recorded, 'rb').read()
        local_data = open(fname, 'rb').read()
        client.publish(topic, payload=local_data, qos=0, retain=False)
        #************* mqtt *************

    play_is_success = True


def detected_callback():
    print("beep START recording...")
    play_beep()


def signal_handler(signal, frame):
    global interrupted
    interrupted = True

def interrupt_callback():
    global interrupted
    return interrupted


# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

detector = snowboydecoder.HotwordDetector(hotword_model, sensitivity=0.5)
print('Listening... Press Ctrl+C to exit')

# main loop
# 1. checks a ring buffer filled with microphone data to see whether a hotword is detected. If yes, call the detected_callback function.
# 2. calls the interrupt_check function: if it returns True, then break the main loop and return.
detector.start(detected_callback = detected_callback,
               audio_recorder_callback = audio_rec_callback,
               interrupt_check = interrupt_callback,
               sleep_time = 0.03,
               silent_count_threshold=10,
               recording_timeout=50)

detector.terminate()
