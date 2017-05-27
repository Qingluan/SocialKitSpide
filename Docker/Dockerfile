FROM ubuntu
MAINTAINER qingluan

RUN cd /etc/apt && mkdir -p ./sources.list.bak && mv sources.list ./sources.list.bak/
COPY sources.list /etc/apt/
RUN uname -a && sleep 1
RUN cat /etc/os-release && sleep 1

RUN apt-get update 
#RUN apt-get install -y python-software-properties
#RUN add-apt-repository ppa:fkrull/deadsnakes
#RUN apt-get update

RUN apt-get install -y python3.5
RUN apt-get install -y python3-pip
RUN apt-get install -y libxml2-dev libxslt1-dev zlib1g-dev

RUN pip3 install SocialKit -i https://pypi.douban.com/simple
RUN pip3 uninstall -y pymongo
RUN pip3 install pymongo -i https://pypi.douban.com/simple
RUN pip3 install chardet -i https://pypi.douban.com/simple
#RUN apt install  -y phantomjs
#RUN apt install -y language-pack-en

RUN pip3 install qtornado --upgrade -i https://pypi.douban.com/simple
#COPY log.py /usr/local/lib/python3.5/dist-packages/Qtornado/log.py

### proxy 
RUN pip3 install shadowsocks -i https://pypi.douban.com/simple


ENV PORT 8088
ENV SHADOW_HOST localhost
ENV SHADOW_PORT 3007
ENV SHADOW_PASS dark1
ENV SHADOW_LOCAL_PORT 1080
ENV SHADOW_METHOD aes-256-cfb
ENV EX only-start-spide


#RUN tar xjf phantomjs-2.1.1-linux-x86_64.tar.bz2
RUN ln -s /opt/phantomjs-2.1.1-linux-x86_64/bin/phantomjs /usr/local/share/phantomjs
RUN ln -s /opt/phantomjs-2.1.1-linux-x86_64/bin/phantomjs /usr/local/bin/phantomjs
RUN ln -s /opt/phantomjs-2.1.1-linux-x86_64/bin/phantomjs /usr/bin/phantomjs

RUN apt install -y libfontconfig1 libfreetype6 libssl-dev chrpath

RUN pip3 install SocialKit --upgrade  -i https://pypi.douban.com/simple
ADD spide.tar.gz /opt/
ADD phantomjs-2.1.1-linux-x86_64.tar.bz2 /opt/

ADD ss-server.json /tmp/
EXPOSE 3007
EXPOSE 3008
EXPOSE 3009

ADD help /usr/bin/

WORKDIR /opt/
WORKDIR /opt/spide
CMD  /usr/local/bin/sslocal -s $SHADOW_HOST -p $SHADOW_PORT  -m $SHADOW_METHOD -k $SHADOW_PASS -l $SHADOW_LOCAL_PORT  -d start &&  /usr/bin/python3  main.py -p $PORT
