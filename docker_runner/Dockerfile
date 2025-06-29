FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y \
    build-essential \
    gcc \
    g++ \
    openjdk-17-jdk \
    python3 \
    python3-pip \
    time \
    curl \
    && apt clean

COPY run_code.sh /scripts/run_code.sh
RUN chmod +x /scripts/run_code.sh

WORKDIR /runner
