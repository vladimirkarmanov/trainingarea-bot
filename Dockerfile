FROM python:3.8.1-alpine

WORKDIR /home/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV HOME=/home/app
ENV APP_HOME=/home/app/src
ENV TELEGRAM_API_TOKEN="905795293:AAE4Hf8Nb0nMh2bohITnWbZ5BInTh5egiN4"

ENV TZ=Asia/Yekaterinburg
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apk update \
    && apk add --virtual .build-deps g++ gcc python3-dev libevent-dev \
    && apk add --no-cache sqlite

RUN pip install --upgrade pip setuptools wheel
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN apk del .build-deps

WORKDIR $APP_HOME

COPY ./media $HOME
COPY ./src $APP_HOME

ENTRYPOINT ["python", "server.py"]
