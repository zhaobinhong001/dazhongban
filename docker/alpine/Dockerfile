FROM alpine
ENV PYTHONUNBUFFERED 1

ADD requirements.txt /requirements.txt
ADD ./pip.conf /root/.pip/pip.conf
RUN echo 'http://mirrors.aliyun.com/alpine/v3.4/main/' > /etc/apk/repositories
RUN echo 'http://mirrors.aliyun.com/alpine/v3.4/community/' >> /etc/apk/repositories

RUN apk update && apk add bash
RUN apk add py-psycopg2 py-gunicorn py-pillow py-pip py-tornado libevent python-dev py-libxml2

RUN pip install --upgrade pip setuptools wheel
RUN pip install -r /requirements.txt