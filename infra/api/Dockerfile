# Build from the repository root: docker build -f infra/api/Dockerfile -t ciai-api:local .
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

RUN useradd --create-home --uid 10001 --shell /usr/sbin/nologin app

COPY infra/api/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt && rm /tmp/requirements.txt

COPY app/__init__.py app/__init__.py
COPY app/api/__init__.py app/api/service.py app/api/ranking.py app/api/schemas_v1.py app/api/schemas.py app/api/mock.py app/api/main.py app/api/
COPY app/api/data/ app/api/data/
COPY data/panel/panel_municipio_mes.csv.gz data/panel/
COPY artifacts/ml/selected_model.joblib artifacts/ml/

USER app
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/api/v1/health', timeout=4).status == 200 else 1)"

CMD ["uvicorn", "app.api.service:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers", "--forwarded-allow-ips", "*"]
