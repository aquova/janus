FROM python:3.11-alpine

RUN apk update && apk add \
    build-base

ADD requirements.txt /janus/requirements.txt
RUN pip install -r /janus/requirements.txt

WORKDIR /janus
CMD ["python", "-u", "janus.py"]
