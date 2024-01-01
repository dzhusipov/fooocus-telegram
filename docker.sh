#!/bin/bash
docker ps | grep fooocus-telegram | awk '{print $1}' | xargs docker stop
docker ps -a | grep fooocus-telegram | awk '{print $1}' | xargs docker rm
docker rmi fooocus-telegram
docker build -t fooocus-telegram .
docker run --restart=always -d --name foocus-telegram-container fooocus-telegram