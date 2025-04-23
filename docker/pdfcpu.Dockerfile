FROM ubuntu:22.04

RUN apt-get update && apt-get install -y wget xz-utils ca-certificates && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

# Download and extract the correct pdfcpu binary for Linux x86_64 in /workspace
RUN wget -O pdfcpu.tar.xz https://github.com/pdfcpu/pdfcpu/releases/download/v0.10.1/pdfcpu_0.10.1_Linux_x86_64.tar.xz \
    && tar -xJf pdfcpu.tar.xz \
    && mv pdfcpu_0.10.1_Linux_x86_64/pdfcpu /usr/local/bin/pdfcpu \
    && chmod +x /usr/local/bin/pdfcpu \
    && rm -rf pdfcpu_0.10.1_Linux_x86_64 pdfcpu.tar.xz

# Ensure config directory exists to avoid runtime errors
RUN mkdir -p /root/.config/pdfcpu

# ENTRYPOINT ["/bin/bash"] 
ENTRYPOINT ["pdfcpu"] 