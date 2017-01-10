FROM python:2.7
ENV PYTHONUNBUFFERED 1

COPY ./docker/bankcard/standard/pip.conf /root/.pip/pip.conf
COPY ./docker/bankcard/standard/app/requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY ./docker/bankcard/standard/app /app

WORKDIR /app

ENTRYPOINT ["python", "server.py"]
