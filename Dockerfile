FROM python:3.9.11-slim

RUN apt-get update
WORKDIR /app

ADD . /app
RUN pip install -r requirements.txt
CMD ["python3", "run.py"]

EXPOSE 5000

