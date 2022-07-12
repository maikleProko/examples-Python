FROM python:3.8

COPY src src
COPY tests tests
WORKDIR src

RUN apt-get update

RUN apt-get install -y avahi-utils iputils-ping
# for dts
RUN apt-get install -y sshpass rsync

RUN pip3 install -r dependency.py.txt

RUN bash ./scripts/dts.sh
RUN bash ./scripts/runtime_docker.sh

CMD ["gunicorn", "--worker-class", "eventlet", "-b", "127.0.0.1:5000", "--timeout", "1000", "app:app"]
