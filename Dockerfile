# ---- Base python ----
FROM python:3.5-alpine

# RUN adduser -D solid_potato

# install dependencies
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev libressl-dev libffi-dev



# Create app directory
WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY app app
COPY migrations migrations
COPY solid_potato.py config.py boot.sh ./

RUN chmod +x boot.sh

ENV FLASK_APP solid_potato.py

ENTRYPOINT ["./boot.sh"]
