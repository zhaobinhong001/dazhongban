FROM python:2.7
ENV PYTHONUNBUFFERED 1

COPY ./pip.conf /root/.pip/pip.conf

COPY ./app/requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY ./app /app

WORKDIR /app

ENTRYPOINT ["python", "server.py"]
