# Free deployment: works on Render, Railway, Fly.io, etc.
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
# Ensure package is importable
ENV PYTHONPATH=/app
EXPOSE 8000
ENV PORT=8000

CMD ["sh", "-c", "uvicorn smart_code_reviewer.app:app --host 0.0.0.0 --port ${PORT}"]
