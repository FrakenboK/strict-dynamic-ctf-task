FROM ubuntu:24.04

RUN apt-get update
RUN apt-get install python3 python3-pip

COPY . /app

WORKDIR /app

RUN python3 -m pip install pyppeteer flask flask[async] 

RUN python3 config/generator.py

RUN mkdir users
RUN mkdir user_notes
RUN mkdir notes

CMD pyppeteer-install

ENTRYPOINT ["python3", "main.py"]
