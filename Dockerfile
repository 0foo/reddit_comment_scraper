FROM python:latest
WORKDIR /scraper
RUN apt-get update
RUN /usr/local/bin/pip3 install requests bs4
ENTRYPOINT []