#!/bin/sh

x-terminal-emulator -e node-red start
x-terminal-emulator -e python audioManagement.py
x-terminal-emulator -e python faceDetection.py
