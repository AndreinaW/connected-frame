#!/bin/sh

cd app/ && docker image build --tag app .
cd ../statistics_service/ && docker image build --tag stats .
cd ../dashboard_service/ && docker image build --tag dashboard .
cd ../commands_service/ && docker image build --tag commands .
docker run -d -p 8080:8080 app
docker run -d -p 8081:8081 stats
docker run -d -p 8082:8082 dashboard
docker run -d -p 8083:8083 commands
