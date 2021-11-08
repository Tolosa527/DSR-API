FROM python:3.9


RUN apt-get update
RUN apt-get upgrade -y

COPY . /app
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN python manage.py makemigrations
RUN python manage.py migrate

RUN python /app/bulkdata.py
