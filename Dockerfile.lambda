# Container used to build AWS lambda packages
FROM amazonlinux:latest

RUN yum -y update && \
    yum -y install \
    python36 \
    python36-devel \
    python36-setuptools \
    python36-pip \
    libtiff \
    libffi-devel \
    gcc \
    openssl-devel

WORKDIR /app/

COPY . /app
