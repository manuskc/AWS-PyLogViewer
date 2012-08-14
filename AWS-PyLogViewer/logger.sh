#! /bin/bash

username="aws-user"
path_to_key="./admin.ssh"

while read server
do
echo "Connectin to server : $server"
ssh -oStrictHostKeyChecking=no -i $path_to_key $username@$server "tail -f /opt/tomcat7/output.log" | ./reader.py &
echo "Connected to server : $server"
done
