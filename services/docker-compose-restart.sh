#!/bin/sh

echo "Restarting"
sh docker-compose-stop.sh
docker run -d -p 8080:8080 app
docker run -d -p 8081:8081 stats
docker run -d -p 8082:8082 dashboard
echo "Successfully restarted!"
