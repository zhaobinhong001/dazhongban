FROM python:2.7.13-alpine
ENV PYTHONUNBUFFERED 1

COPY ./docker/business/standard/pip.conf /root/.pip/pip.conf
COPY ./docker/business/standard/app/requirements.txt /requirements.txt
COPY ./docker/business/standard/app /app

RUN pip install -r /requirements.txt
RUN cd /app && python manage.py db upgrade

WORKDIR /app

ENTRYPOINT ["python", "server.py"]
