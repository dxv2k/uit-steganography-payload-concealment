FROM ubuntu:22.04
RUN apt-get update && apt-get install -y bash netcat python3 wget && rm -rf /var/lib/apt/lists/*
WORKDIR /workspace
COPY . /workspace 