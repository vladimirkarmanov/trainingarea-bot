FROM python:3.8.1-alpine

WORKDIR /home/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV TELEGRAM_API_TOKEN="905795293:AAE4Hf8Nb0nMh2bohITnWbZ5BInTh5egiN4"

ENV TZ=Asia/Yekaterinburg
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt update && apt install sqlite3
RUN pip install --upgrade pip
COPY ./requirements.txt ./
RUN pip install --no-cache -r requirements.txt

COPY ./media ./media
COPY ./src ./src

ENTRYPOINT ["python3", "src/server.py"]
