#!/usr/bin/env bash

sudo chown -R kir:kir *
sudo find . -name '.pytest_cache' -exec rm -rf {} \;
sudo find . -name '__pycache__' -exec rm -rf {} \;
sudo find . -name '*.pyc' -exec rm -rf {} \;
sudo find . -name '*.log' -exec rm -rf {} \;
sudo find . -name 'nistest.egg-info' -exec rm -rf {} \;
rm -rf ./nis-test/pytest/report/*
rm -rf ./nis-test/pytest/allure/*
rm -rf ./nis-test/pytest/lib/dist/*

container=$1
echo 'container: '$container
container_id=`docker ps -a | grep $container | awk '{print $1}'`
image_id=`docker images | grep $container | awk '{print $3}'`
echo 'container_id: '$container_id
echo 'image_id: '$image_id
echo 'stopping container...'
docker stop $container_id
echo 'delete container...'
docker rm $container_id
echo 'delete image...'
docker rmi -f $image_id
echo 'start container...'
docker-compose up -d $container
