FROM python:3.8-buster

ADD ./requirements.txt /tmp/requirements.txt

RUN pip3 install --no-cache-dir -q -r /tmp/requirements.txt

ADD . /opt/comcon/
WORKDIR /opt/comcon

RUN adduser --disabled-password kevin_as
USER kevin_as

CMD python3 main.py -j