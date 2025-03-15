# Stage 1: Vendor dependencies
FROM python:3.9-slim as vendor

WORKDIR /vendor

RUN apt-get update && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*

# Install Poetry and required plugin
RUN pip install poetry poetry-plugin-export

# Copy project files
COPY pyproject.toml poetry.lock ./

# Export and download dependencies
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes && \
    pip download -r requirements.txt -d .

# Stage 2: Build PPA package
FROM ubuntu:22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    OUTPUT_DIR="/output" \
    PATH="/root/.local/bin:${PATH}"

# Install build dependencies
RUN apt-get update && \
    apt-get install -y \
    devscripts \
    dh-python \
    build-essential \
    python3-all \
    python3-pip \
    python3-venv \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create build directory
WORKDIR /build

# Copy scripts and vendored dependencies
COPY .ci/build-ppa/prepare-debian.py /usr/local/bin/prepare-debian
COPY .ci/build-ppa/build-ppa.sh /usr/local/bin/build-ppa.sh
COPY --from=vendor /vendor /vendor
RUN chmod +x /usr/local/bin/prepare-debian /usr/local/bin/build-ppa.sh

# Ensure output is externally accessible
VOLUME ["/output"]

# Main entry point
CMD ["build-ppa.sh"]
