FROM alpine
ENV PYTHONUNBUFFERED 1

# Requirements have to be pulled and installed here, otherwise caching won't work
COPY ./requirements.txt /requirements.txt

RUN echo 'http://mirrors.aliyun.com/alpine/v3.4/main/' > /etc/apk/repositories
RUN apk update && apk add bash 
RUN apk add py-psycopg2 py-gunicorn py-pillow py-pip py-tornado libevent python-dev py-libxml2
RUN pip install --upgrade pip setuptools wheel -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com 

RUN pip install -r /requirements.txt
RUN addgroup -S django && adduser -S -G django django

COPY . /app

RUN chown -R django /app
RUN pip install django_seed && python /app/manage.py migrate

COPY ./docker/django/gunicorn.sh /gunicorn.sh
COPY ./docker/django/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r//' /entrypoint.sh \
    && sed -i 's/\r//' /gunicorn.sh \
    && chmod +x /entrypoint.sh \
    && chown django /entrypoint.sh \
    && chmod +x /gunicorn.sh \
    && chown django /gunicorn.sh

WORKDIR /app

ENTRYPOINT ["/entrypoint.sh"]
