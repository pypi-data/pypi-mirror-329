ARG PYTHONVER=3.11
ARG DISTRO=bookworm
## Base build stage for Slidge, prepares and installs common dependencies.
FROM ghcr.io/astral-sh/uv:python$PYTHONVER-$DISTRO AS builder-base
ARG PYTHONVER
ENV PATH="/venv/bin:$PATH"

# rust/cargo is for building "cryptography" since they don't provide wheels for arm32
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    build-essential \
    ca-certificates \
    cargo \
    curl \
    git \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    pkg-config \
    python3-dev \
    rustc

RUN uv venv /venv
WORKDIR /build
# Only copy files used to define dependencies, so this step can be in cache
# as long as we don't touch the deps.
COPY uv.lock pyproject.toml /build/

FROM builder-base AS builder
RUN uv export --no-dev > requirements.txt
RUN uv pip install --requirement requirements.txt
RUN ln -s /venv/lib/python$PYTHONVER /venv/lib/python

# CI environment for slidge
FROM builder-base AS woodpecker-slidge
# In CI we sometimes move /venv to .venv, then update it for the whole workflow.
ENV PATH=".venv/bin:$PATH"
RUN uv export > requirements.txt
RUN uv pip install --requirement requirements.txt

## Minimal runtime environment for slidge
# We re-use this for plugins that need extra dependencies, but copy the ./slidge
# dir as the last step to be docker cache-friendly
FROM docker.io/library/python:$PYTHONVER-slim AS base
ARG PYTHONVER
ENV PATH="/venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

# libmagic1: to guess mime type from files
# media-types: to determine file name suffix based on file type
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    libmagic1 media-types shared-mime-info python3-slixmpp-lib

RUN addgroup --system --gid 10000 slidge
RUN adduser --system --uid 10000 --ingroup slidge --home /var/lib/slidge slidge

ENV SLIDGE_LEGACY_MODULE=legacy_module

WORKDIR /var/lib/slidge
COPY --from=builder /venv /venv
# hacky, link compiled (fast) stringprep.so to the proper dir
RUN ln -s /usr/lib/python3/dist-packages/slixmpp/stringprep*.so /venv/lib/python$PYTHONVER/site-packages/slixmpp/

STOPSIGNAL SIGINT
USER slidge

ENTRYPOINT ["python", "-m", "slidge"]

# dev container with hot reload on code change
FROM base AS dev

USER root

COPY --from=codeberg.org/slidge/prosody-slidge-dev:latest \
  /etc/prosody/certs/localhost.crt \
  /usr/local/share/ca-certificates/
RUN update-ca-certificates

RUN pip install watchdog[watchmedo]

COPY --from=builder /venv /venv
COPY ./slidge /venv/lib/python/site-packages/slidge

ENTRYPOINT ["watchmedo", "auto-restart", \
  "--pattern", "*.py", \
  "--directory", "/venv/lib/python/site-packages/legacy_module/", \
  "--recursive", \
  "python", "--", "-m", "slidge", \
  "--jid", "slidge.localhost", \
  "--secret", "secret", \
  "--debug", \
  "--upload-service", "upload.localhost", \
  "--admins", "test@localhost", \
  "--dev-mode"]
