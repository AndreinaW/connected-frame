# coding=utf-8
import snowboydecoder
import signal
import paho.mqtt.client as mqtt
import audio

#************* mqtt *************
mosquitto_mqtt_broker_ip = 'localhost'
mosquitto_mqtt_broker_port = '1883'

mosquitto_mqtt_broker_url = mosquitto_mqtt_broker_ip + ':' + mosquitto_mqtt_broker_port
topic = 'audio/register'

client = mqtt.Client()
client.connect(mosquitto_mqtt_broker_ip, int(mosquitto_mqtt_broker_port), 60)
print('Mosquitto MQTT Broker url: ' + mosquitto_mqtt_broker_url)

#************* mqtt *************

interrupted = False
hotword_model = "./resources/ConnectedFrame.pmdl"
beep_audio = "./resources/ding.wav"


def audio_rec_callback(fname):
    audioplayed = audio.play_audio(beep_audio)
    audioplayed = audio.play_audio(fname)   # todo: erase this

    #if audioplayed:
    print("publish to topic")
    #************* mqtt *************
    local_data = open(fname, 'rb').read()
    client.publish(topic, payload=local_data, qos=0, retain=False)
    #************* mqtt *************

    print('\n\nListening... Press Ctrl+C to exit')


def detected_callback():
    audio.play_audio(beep_audio)

def signal_handler(signal, frame):
    global interrupted
    interrupted = True

def interrupt_callback():
    global interrupted
    return interrupted


# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

detector = snowboydecoder.HotwordDetector(hotword_model, sensitivity=0.5)
print('\n\nListening... Press Ctrl+C to exit')

# main loop
# 1. checks a ring buffer filled with microphone data to see whether a hotword is detected. If yes, call the detected_callback function.
# 2. calls the interrupt_check function: if it returns True, then break the main loop and return.
detector.start(detected_callback = detected_callback,
               audio_recorder_callback = audio_rec_callback,
               interrupt_check = interrupt_callback,
               sleep_time = 0.03,
               silent_count_threshold=10,
               recording_timeout=40)

detector.terminate()