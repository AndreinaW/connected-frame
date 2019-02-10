FROM python:alpine3.7

COPY . /app
WORKDIR /app
RUN pip3 install --upgrade watson-developer-cloud
EXPOSE 8080

CMD ["python", "-u", "app.py"]