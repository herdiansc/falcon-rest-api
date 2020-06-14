FROM python:3.6.2

ADD requirements.txt /app/
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ADD . /app

COPY start.sh /scripts/start.sh
ENTRYPOINT ["sh","/scripts/start.sh"]