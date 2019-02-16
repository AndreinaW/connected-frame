# coding=utf-8
import subprocess
from threading import Thread

thread = None
adresse_mac_speakers = "78:44:05:DA:56:65"


def play_audio_thread(audio_path):
    # with .call if there is an error while executing the command; It won't make an exception and stop executing the .py
    subprocess.call(['aplay', '-D', 'bluealsa:DEV=' + adresse_mac_speakers, audio_path])
    #subprocess.call(['aplay', audio_path])         # TODO: erase


# Create and run the thread to play the audio
# wait: True wait for audio to finish playing to continue execution. False don't wait. Default is True
# returns True if playing and false if not
def play_audio(audio_path, wait = True):
    global thread
    print('')

    if thread != None and thread.is_alive():
        print("Already playing something...")
        return False

    thread = Thread(target = play_audio_thread, args=[audio_path])
    thread.start()
    print("playing audio...")

    if wait:
        thread.join()
        print("finished playing audio...\n")

    return True