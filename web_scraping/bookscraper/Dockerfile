# Usa una imagen de Python como base
FROM python:3.9-slim
WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/tf_creds.json
CMD ["scrapy", "crawl", "casaspider"]
