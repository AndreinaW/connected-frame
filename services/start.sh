#!/bin/sh

cd app/ && x-terminal-emulator -e python3 app.py
cd ../statistics_service/ && x-terminal-emulator -e python3 statistics_service.py
cd ../dashboard_service/ && x-terminal-emulator -e python3 dashboard_service.py
cd ../commands_service/ && x-terminal-emulator -e python3 commands_service.py