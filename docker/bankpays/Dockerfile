FROM python:2.7.13-alpine
ENV PYTHONUNBUFFERED 1

COPY ./docker/bankpays/standard/pip.conf /root/.pip/pip.conf
COPY ./docker/bankpays/standard/app/requirements.txt /requirements.txt
COPY ./docker/bankpays/standard/app /app

RUN pip install -r /requirements.txt

WORKDIR /app

ENTRYPOINT ["python", "manage.py", "runserver"]
