FROM python:3.10-alpine

COPY . /app

WORKDIR /app

RUN python3 -m pip install -r requirements.txt

RUN python3 config/generator.py

RUN mkdir users
RUN mkdir user_notes
RUN mkdir notes

CMD pyppeteer-install

ENTRYPOINT ["python3", "main.py"]