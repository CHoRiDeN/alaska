FROM python:3

WORKDIR /deploy
COPY start.sh /deploy
COPY crontab_scrapper /deploy
COPY requirements.txt /deploy
RUN chmod +x /deploy/start.sh

RUN pip install -r /deploy/requirements.txt
RUN pip install requests
RUN pip install flask-cors

ENTRYPOINT /deploy/start.sh
