FROM ubuntu:18.04

LABEL maintainer="hebehh@gmail.com"

ENV UID 2500
ENV GID 2000

RUN groupadd -g ${GID} appuser
RUN useradd -u ${UID} -g ${GID} appuser

RUN apt-get update && apt-get install -y python3-pip libpq-dev\
	&& apt-get install -y systemd language-pack-en libjpeg-dev libpng-dev build-essential locales\
	&& apt-get install -y python3-dev default-libmysqlclient-dev libpcre3 libpcre3-dev libssl-dev libffi-dev \
	&& apt-get install -y uwsgi uwsgi-plugin-python3 \
	&& ln -fs /usr/share/zoneinfo/Asia/Singapore /etc/localtime && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata

RUN echo "net.core.somaxconn = 2048" >> /etc/sysctl.conf
ADD requirements.txt requirements.txt
RUN pip3 install --trusted-host pypi.python.org -r requirements.txt

USER appuser

WORKDIR /app
ADD --chown=${UID}:${GID} ./Server /app

EXPOSE 5000

CMD ["uwsgi", "--ini", "wsgi.ini"]
