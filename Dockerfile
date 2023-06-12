FROM python:3.8-slim
COPY requirements.txt /
RUN pip3 install -r /requirements.txt
COPY . /app
WORKDIR /app
RUN chmod +x gunicorn_start.sh
ENTRYPOINT ["./gunicorn_start.sh"]