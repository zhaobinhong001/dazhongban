FROM python:2.7
ENV PYTHONUNBUFFERED 1

COPY ./docker/bankcard/pip.conf /root/.pip/pip.conf
COPY ./docker/bankcard/app/requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY ./docker/bankcard/app /app

WORKDIR /app

ENTRYPOINT ["python", "server.py"]
