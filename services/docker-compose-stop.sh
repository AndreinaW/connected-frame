#!/bin/sh

echo "Stopping frampeplus docker..."
docker stop app
docker stop stats
docker stop dashboard
echo "Frameplus docker stopped!"
