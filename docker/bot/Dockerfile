FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

COPY app /app
COPY ../.env /.env

ENV DATABASE_HOST=192.168.0.4
ENV DATABASE_PORT=53306
ENV DATABASE_NAME=bonusmoney

ENTRYPOINT ["python"]
CMD ["bot.py"]