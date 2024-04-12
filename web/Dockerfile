FROM python:3.10-alpine

RUN adduser --disabled-password -u 1001 user

COPY --chown=user:user . /app

WORKDIR /app

USER user

RUN python3 -m pip install -r requirements.txt

RUN python3 config/generator.py

RUN mkdir users
RUN mkdir user_notes
RUN mkdir notes

ENTRYPOINT ["python3", "main.py"]