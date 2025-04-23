FROM ubuntu:22.04
RUN apt-get update && apt-get install -y netcat bash && rm -rf /var/lib/apt/lists/*
WORKDIR /workspace
COPY . /workspace 