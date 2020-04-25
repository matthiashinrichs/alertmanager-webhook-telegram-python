FROM alpine:3.7

LABEL maintainer="Matthias Hinrichs <matthias.hinrichs@me.com>"

WORKDIR /alertmanager-webhook-telegram

COPY requirements.txt requirements.txt
COPY alertmanager-webhook-telegram-python/flaskAlert.py flaskAlert.py 
COPY run.sh run.sh

RUN apk update \
                && apk add bash gcc python3-dev musl-dev libffi-dev openssl-dev \
                && rm -rf /var/cache/apk/* \
                && pip3 --no-cache-dir install -r requirements.txt \
                && chmod +x run.sh

EXPOSE 9119

ENTRYPOINT ["./run.sh"]
