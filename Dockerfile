FROM python:3.8-buster AS pybase
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

FROM pybase AS py-only-base
COPY . . 

FROM py-only-base AS http
EXPOSE 8000
CMD ["python", "-u", "main.py"]

FROM py-only-base AS bot
CMD ["python", "-u", "asyncchatbot.py"]

FROM py-only-base AS cron
CMD ["python", "-u", "schedulemanager.py"]


FROM pybase AS all-in-one
RUN apt-get update
RUN apt-get install -y redis
RUN apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false

COPY . . 
EXPOSE 8000
CMD ["bash", "run-all.sh"]


