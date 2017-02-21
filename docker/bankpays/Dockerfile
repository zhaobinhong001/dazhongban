FROM python:2.7.13-alpine
ENV PYTHONUNBUFFERED 1

COPY ./docker/bankpays/standard/pip.conf /root/.pip/pip.conf
COPY ./docker/bankpays/standard/app/requirements.txt /requirements.txt
COPY ./docker/bankpays/standard/app /app

COPY ./docker/bankpays/gunicorn.sh /gunicorn.sh
COPY ./docker/bankpays/entrypoint.sh /entrypoint.sh

RUN sed -i 's/\r//' /entrypoint.sh
RUN sed -i 's/\r//' /gunicorn.sh

RUN chmod +x /entrypoint.sh
RUN chmod +x /gunicorn.sh

RUN pip install -r /requirements.txt

WORKDIR /app

ENTRYPOINT ["/entrypoint.sh"]
