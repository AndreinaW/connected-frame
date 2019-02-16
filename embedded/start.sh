#!/bin/sh

node-red start &
# bash -c "exec -a faceDec python faceDetection.py &"
cd audio/
bash -c "exec -a audioRec python audioRecording.py"
