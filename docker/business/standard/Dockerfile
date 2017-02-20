FROM python:2.7
ENV PYTHONUNBUFFERED 1

COPY ./pip.conf /root/.pip/pip.conf
COPY ./app /app

RUN pip install -r /app/requirements.txt
RUN cd /app && python manage.py db upgrade

WORKDIR /app

ENTRYPOINT ["python", "server.py"]
