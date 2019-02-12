FROM python:alpine3.7

COPY . /app
WORKDIR /app

RUN pip3 install --upgrade watson-developer-cloud
RUN pip3 install --upgrade paho-mqtt
RUN pip3 install --upgrade requests

EXPOSE 8080

CMD ["python", "-u", "app.py", "192.168.1.125"]