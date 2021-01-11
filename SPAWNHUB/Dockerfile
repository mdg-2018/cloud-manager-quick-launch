FROM ubuntu:18.04
LABEL maintainer="chris@grabosky.net"
LABEL version="1.1.26"
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
        python3-distutils \
        unzip \
        dos2unix \
        curl \
        software-properties-common \
        python-apt

# force newer version of ansible
# this must be first before 3.7 change...
RUN ln -s /usr/bin/python3.6 /usr/bin/python3 -f
RUN add-apt-repository -y ppa:ansible/ansible
RUN apt-get update && apt-get install -y ansible

# force specific version of python 3.7
RUN ln -s /usr/bin/python3.7 /usr/bin/python3 -f

# install pip
RUN wget -O get-pip.py https://bootstrap.pypa.io/get-pip.py
RUN python3 get-pip.py

# install pip required packages
RUN python3 -m pip install dnspython pymongo tornado requests six docker boto3 boto

# install aws cli
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip
RUN ./aws/install

# copy over Blazor WASM front end and calls backend python API
COPY ./SpawnHub /opt/wwwroot
COPY ./SpawnHubSPA/bin/Release/netstandard2.1/publish/wwwroot /opt/wwwroot/static
COPY ./AnsibleContent /opt/AnsibleContent
COPY ./credentials /root/.aws/credentials
COPY ./awsconfig /root/.aws/config
RUN dos2unix /opt/AnsibleContent/tls/generateTLS/*; dos2unix /opt/AnsibleContent/src/*
RUN mkdir -p /opt/AnsibleContent/tls/generateTLS/keys/out
RUN mkdir -p /opt/AnsibleContent/connections
RUN chmod 600 /opt/AnsibleContent/key.pem

# web server is python tornado which also powers API and runs on port 8000
CMD ["python3", "/opt/wwwroot/SpawnHub/__init__.py"]
#CMD ["/bin/bash"]

EXPOSE 8000
