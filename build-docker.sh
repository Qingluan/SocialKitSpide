#!/bin/bash
cd Docker;
docker -v  1>/dev/null 2>&1  && printf "[+] check docker\n";
tar -czf spide.tar.gz spide && printf "[+] tar web project \n";
docker build -t social-spide . &&  printf "[+] build images ok  'docker images ' to see ....\n";

if [ $? -eq 0 ];then
    rm spide.tar.gz
    printf "[+] build ok then rm tmp file"
fi
