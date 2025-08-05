FROM python:3.11-slim

# Prevents Python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr 
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    wget \
    ncbi-blast+ \
    && rm -rf /var/lib/apt/lists/*

# Install isPcr (try multiple approaches for compatibility)
RUN apt-get update && \
    # Try to install isPcr from source or pre-compiled binary
    wget -O /usr/local/bin/isPcr \
    https://github.com/UCSC-Browser/kent/raw/master/bin/linux/isPcr || \
    # Fallback: install from UCSC utilities
    wget -O /usr/local/bin/isPcr \
    http://hgdownload.cse.ucsc.edu/admin/exe/linux.x86_64/isPcr || \
    # If still fails, create a stub that shows helpful error
    echo '#!/bin/bash' > /usr/local/bin/isPcr && \
    echo 'echo "ERROR: isPcr not available. Use --workflow blast instead of --workflow pcr"' >> /usr/local/bin/isPcr && \
    echo 'exit 1' >> /usr/local/bin/isPcr && \
    chmod +x /usr/local/bin/isPcr && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    emmtyper

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

COPY . .
RUN pip install --no-deps .

USER emmtyper
