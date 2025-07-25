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

RUN mkdir -p /scripts && chmod 755 /scripts
COPY run_code.sh /scripts/run_code.sh

# DO NOT 777 /runner, let docker control perms securely
WORKDIR /runner
