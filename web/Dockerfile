FROM python:3.10-alpine

WORKDIR /app

COPY . /app

RUN python3 -m pip install -r requirements.txt

RUN pyppeteer-install

ENTRYPOINT ["python3", "main.py"]