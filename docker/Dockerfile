FROM python:3.10

ENV TZ=America/Sao_Paulo
ENV MEDIA_PATH_ON_DOCKER=/app/data
ENV WORKING_DIR=/app
WORKDIR ${WORKING_DIR}

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        tzdata wget unzip ca-certificates curl \
        fonts-liberation libasound2 libnss3 libxss1 libgbm1 && \
    ln -fs /usr/share/zoneinfo/$TZ /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata && \
    wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get install -y ./google-chrome-stable_current_amd64.deb && \
    rm -f google-chrome-stable_current_amd64.deb && \
    rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

# ---- Copy only dependency files / metadata ----
COPY pyproject.toml uv.lock* README.md ./

# ---- Create venv and install deps with uv ----
ENV UV_PROJECT_ENVIRONMENT=/venv
RUN uv sync --no-dev --frozen

# ---- Copy the rest of the source ----
COPY . ${WORKING_DIR}

ENV PYTHONPATH=src
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1

CMD ["/venv/bin/python", "src/automacao_certificados/main.py"]

