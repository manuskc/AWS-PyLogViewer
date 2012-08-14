#!/bin/bash

mongodb="PATH TO MONGO DB INSTALLATION DIRECTORY / BIN";
dbpath="PATH TO MONGO DB DATA DIRECTORY"

sh -c "$mongodb/mongod --dbpath=$dbpath" &
sleep 5
sudo cat servers.txt | ./logger.sh &
sleep 5
python ./display.py &
