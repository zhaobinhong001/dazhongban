FROM python:2.7
ENV PYTHONUNBUFFERED 1

COPY ./pip.conf /root/.pip/pip.conf
COPY ./app /app

RUN pip install -r /app/requirements.txt

WORKDIR /app

ENTRYPOINT ["python", "manage.py", "runserver"]
