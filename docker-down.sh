#!/bin/bash

docker container rm postgres redis rabbitmq food-api consumer --force
docker network rm my-network
