FROM python:3.8-slim-buster

RUN useradd -ms /bin/bash appuser
USER appuser

MAINTAINER Kevin McGrath "kevin.mcgrath@symphony.com"

ADD ./requirements.txt /tmp/requirements.txt

RUN pip3 install --no-cache-dir -q -r /tmp/requirements.txt

ADD . /opt/comcon/
WORKDIR /opt/comcon

CMD python3 main.py -j