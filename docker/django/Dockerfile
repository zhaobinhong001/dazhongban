# FROM alpine
FROM bankeys:alpine
ENV PYTHONUNBUFFERED 1

COPY . /app
COPY ./env.docker /app/.env
COPY ./docker/django/pip.conf /root/.pip/pip.conf
COPY ./docker/django/Procfile /app/Procfile

RUN echo 'http://mirrors.aliyun.com/alpine/v3.4/main/' > /etc/apk/repositories
RUN echo 'http://mirrors.aliyun.com/alpine/v3.4/community/' >> /etc/apk/repositories

RUN apk update && apk add bash curl
RUN apk add py-psycopg2 py-gunicorn py-pillow py-pip py-tornado libevent python-dev py-libxml2

RUN pip install --upgrade pip setuptools wheel
RUN pip install -r /app/requirements.txt
RUN pip install /app/rongcloud.zip

RUN addgroup -S django && adduser -S -G django django
RUN chown -R django /app

#RUN DJANGO_SETTINGS_MODULE=config.settings.prod python /app/manage.py migrate

COPY ./docker/django/gunicorn.sh /gunicorn.sh
COPY ./docker/django/entrypoint.sh /entrypoint.sh

RUN sed -i 's/\r//' /entrypoint.sh
RUN sed -i 's/\r//' /gunicorn.sh

RUN chmod +x /entrypoint.sh
RUN chmod +x /gunicorn.sh

RUN chown django /entrypoint.sh
RUN chown django /gunicorn.sh

WORKDIR /app

ENTRYPOINT ["/entrypoint.sh"]
