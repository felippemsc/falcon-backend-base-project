FROM python:3.7.1-alpine3.7

ARG version

ENV API_VERSION=$version

EXPOSE 8080

RUN apk add --no-cache postgresql-dev gcc python3-dev musl-dev curl-dev

COPY . app
WORKDIR app
RUN pip install -r requirements.txt

CMD gunicorn -w 4 -b 0.0.0.0:8080 --log-config logging.ini main:app