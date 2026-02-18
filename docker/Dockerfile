FROM python:slim-trixie
LABEL maintainer="Darius Stefan <darius.stefan@opensips.org>"

RUN pip install opensips

ADD "run.sh" "/run.sh"

ENV PYTHONPATH=/usr/lib/python3/dist-packages

ENTRYPOINT [ "/run.sh" ]
