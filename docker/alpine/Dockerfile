FROM alpine
ENV PYTHONUNBUFFERED 1

RUN echo 'http://mirrors.aliyun.com/alpine/v3.4/main/' > /etc/apk/repositories

RUN apk update && apk add bash 
RUN apk add py-psycopg2 py-gunicorn py-pillow py-pip py-tornado libevent python-dev

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
RUN addgroup -S django && adduser -S -G django django

COPY . /app
RUN chown -R django /app

WORKDIR /app
