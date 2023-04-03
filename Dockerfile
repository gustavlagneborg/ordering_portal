# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

RUN apt-get update && apt-get install -y \
    libxrender1 \
    libfontconfig1 \
    libxtst6 \
    wkhtmltopdf \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /ordering_portal

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]