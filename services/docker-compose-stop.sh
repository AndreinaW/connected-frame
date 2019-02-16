#!/bin/sh

echo "Stopping frampeplus docker..."
docker stop app
docker stop stats
docker stop dashboard
docker stop commands
echo "Frameplus docker stopped!"

# docker stop $(docker ps -a -q)