FROM python:3.11.3

COPY . /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install -r requirements.txt

ENTRYPOINT python api.py
