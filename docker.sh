#!/bin/bash
git pull
docker ps | grep fooocus-telegram | awk '{print $1}' | xargs docker stop || true
docker ps -a | grep fooocus-telegram | awk '{print $1}' | xargs docker rm || true
docker rmi fooocus-telegram || true
docker build -t fooocus-telegram .
docker run --restart=always -d --name foocus-telegram-container fooocus-telegram