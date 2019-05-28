FROM python:3.7
MAINTAINER Norbiox
RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
ADD app /app/
