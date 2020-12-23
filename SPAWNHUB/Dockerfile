# bespoke replacement for jupyter hub to meet the needs of MongoDB SAs
# this provides a UI and REST API to launch containers of the 
# 979559056307.dkr.ecr.us-east-1.amazonaws.com/mongodb-sa-jupyter container for individual environments for each SA
FROM ubuntu:18.04
LABEL maintainer="chris@grabosky.net"
LABEL version="1.1.0"
ENV CONTAINER_SHELL=bash
ENV CONTAINER=

ARG DEBIAN_FRONTEND=noninteractive
ENV DEBIAN_FRONTEND=noninteractive

# basic app installs
RUN apt-get clean && \
    apt-get update && \
    apt-get install -y \
        git \
        whois \
        python3.7 \
        gnupg2 \
        wget \
        vim \
        python3-distutils

# add docker CLI to apt and install it
RUN apt-get install -y apt-transport-https ca-certificates curl software-properties-common
RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
RUN add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"
RUN apt update && apt install -y docker-ce

# force specific version of python 3.7
RUN ln -s /usr/bin/python3.7 /usr/bin/python3 -f

# install pip
RUN wget -O get-pip.py https://bootstrap.pypa.io/get-pip.py
RUN python3 get-pip.py

# install pip required packages
RUN python3 -m pip install dnspython pymongo tornado requests six docker

# copy over Blazor WASM front end and calls backend python API
COPY ./SpawnHub /opt/wwwroot
COPY ./SpawnHubSPA/bin/Debug/netstandard2.1/publish/wwwroot /opt/wwwroot/static

# web server is python tornado which also powers API and runs on port 8000
CMD ["python3", "/opt/wwwroot/SpawnHub/__init__.py"]
#CMD ["/bin/bash"]

EXPOSE 8000
