#!/bin/bash

docker -v  1>/dev/null 2>&1  && printf "[+] check docker\n";
tar -czf spide.tar.gz spide && printf "[+] tar web project \n";
docker build -t social-spide . &&  printf "[+] build images ok  'docker images ' to see ....\n";

