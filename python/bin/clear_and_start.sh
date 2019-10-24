#!/usr/bin/env bash

docker-compose down

#sudo rm -rf logs/*

ids='tests kafka confl redis'

for id in $ids
do
    echo 'id: '$id
    images=$(docker images | grep $id | awk '{print $3}')
    containers=$(docker container list | grep $id | awk '{print $1}')
    echo 'images: '$images
    echo 'containers: '$containers
    docker rmi $images --force
    docker rm $containers --force
done

docker-compose up -d --build



