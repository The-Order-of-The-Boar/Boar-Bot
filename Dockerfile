FROM alpine:3.14

RUN \
    apk update && \
    apk upgrade  && \
    apk add python3 py3-pip py3-requests py3-pillow py3-dateutil py3-psycopg2 && \
    apk add py3-aiohttp && \
    pip install discord.py

COPY . /app
WORKDIR /app

CMD ["python3", "bot.py"]
