FROM ubuntu:18.04

LABEL maintainer="hebehh@gmail.com"
USER root


RUN apt-get update && apt-get install -y python3-pip libpq-dev\
	&& apt-get install -y systemd language-pack-en libjpeg-dev libpng-dev build-essential locales\
	&& apt-get install -y python3-dev default-libmysqlclient-dev libpcre3 libpcre3-dev libssl-dev libffi-dev \
	&& apt-get install -y uwsgi uwsgi-plugin-python3 \
	&& ln -fs /usr/share/zoneinfo/Asia/Singapore /etc/localtime && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata

ADD requirements.txt requirements.txt
RUN pip3 install --trusted-host pypi.python.org -r requirements.txt

WORKDIR /app
ADD ./Server /app

EXPOSE 80

CMD ["uwsgi", "--ini", "wsgi.ini"]
