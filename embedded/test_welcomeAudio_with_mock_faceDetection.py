# coding=utf-8
import signal
import time
import sys
sys.path.insert(0, './audio')
import audio

run = True
def signal_handler(signal, frame):
	global run
	run = False
# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)
print('Listening... Press Ctrl+C to exit')
i = 0




isFirstDetection = False
isWelcomePlayed = False
welcome_audio = "./audio/resources/welcome.wav"



while run:
	print(i)

	if i > 50:
		print ('Face DETECTED!')

		if not isFirstDetection:
			print("First detection...")
			isFirstDetection = True
			isWelcomePlayed = audio.play_audio(welcome_audio)
			print(isWelcomePlayed)
			# while not isWelcomePlaying:
			# 	isWelcomePlaying = audio.play_audio(welcome_audio)

		# if the face was detected for the first time but for some reason the welcome audio
		# was not played then try to play it again
		elif isFirstDetection and not isWelcomePlayed:
			isWelcomePlayed = audio.play_audio(welcome_audio)

		time.sleep(3)
	else:
		isFirstDetection = False


	i += 1
	if i > 53:
		i = 0

