FROM ubuntu

# The below env is to allow graphviz to be installed properly as otherwise there are issues with terminal inputs
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -y update && apt-get install -y pipenv python3 graphviz && pip3 install diagrams rerun

WORKDIR /data

ENTRYPOINT [ "rerun" ]
