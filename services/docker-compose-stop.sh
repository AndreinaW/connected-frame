#!/bin/sh

echo "Stopping frampeplus docker..."
docker stop $(docker ps -a -q)
echo "Frameplus docker stopped!"
