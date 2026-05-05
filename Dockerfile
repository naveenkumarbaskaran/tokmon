FROM python:3.12-slim AS builder

WORKDIR /app
COPY pyproject.toml README.md LICENSE ./
COPY src/ src/

RUN pip install --no-cache-dir ".[all]"

FROM python:3.12-slim

LABEL maintainer="Naveen Kumar Baskaran <naveenkb142@gmail.com>"
LABEL org.opencontainers.image.source="https://github.com/naveenkumarbaskaran/tokmon"
LABEL org.opencontainers.image.description="Lightweight LLM token and cost tracker"
LABEL org.opencontainers.image.licenses="MIT"

WORKDIR /app
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin/tokmon /usr/local/bin/tokmon

ENTRYPOINT ["tokmon"]
CMD ["--help"]
