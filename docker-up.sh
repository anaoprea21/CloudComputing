#!/bin/bash

docker network create my-network

docker run \
	--name postgres \
	--network my-network \
	--publish 5432:5432 \
	-e POSTGRES_DB=db \
	-e POSTGRES_PASSWORD=my-secret-pw \
	-d \
	postgres

docker run \
	--name redis \
	--network my-network \
	--publish 6379:6379 \
	-d \
	redis --bind 0.0.0.0

docker run \
	--name rabbitmq \
	--network my-network \
	--publish 5672:5672 \
	-d \
	rabbitmq

docker build . --tag food-api
docker run \
	--name food-api \
	--network my-network \
	--publish 8000:8000 \
	-e DB_HOST="postgres" \
	-e DB_NAME="db" \
	-e DB_USERNAME="postgres" \
	-e DB_PASSWORD="my-secret-pw" \
	-e REDIS_HOST="redis" \
	-e REDIS_DATABASE="0" \
	-e RABBITMQ_HOST="rabbitmq" \
	-d \
	food-api:latest

docker build -f ./Dockerfile-consumer . --tag consumer
docker run \
	--name consumer \
	--network my-network \
	-e DB_HOST="postgres" \
	-e DB_NAME="db" \
	-e DB_USERNAME="postgres" \
	-e DB_PASSWORD="my-secret-pw" \
	-e RABBITMQ_HOST="rabbitmq" \
	-d \
	consumer:latest
