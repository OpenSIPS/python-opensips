FROM python:3.9-slim-buster
LABEL maintainer="Darius Stefan <darius.stefan@opensips.org>"

RUN apt-get -y update -qq && \
    apt-get -y install git

RUN git clone https://github.com/OpenSIPS/python-opensips.git /usr/src/python-opensips && \
    cd /usr/src/python-opensips && \
    python3 setup.py install &&\
    cd / && rm -rf /usr/src/python-opensips

RUN apt-get purge -y git && \
    apt-get autoremove -y && \
    apt-get clean

ADD "run.sh" "/run.sh"

ENV PYTHONPATH=/usr/lib/python3/dist-packages

ENTRYPOINT [ "/run.sh" ]
