FROM python:3.11-slim

WORKDIR /app

COPY /requirements.txt .
COPY wait-for-model-download.sh .
RUN chmod +x wait-for-model-download.sh

RUN apt-get update && apt-get install -y curl

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .
COPY templates/ templates/

EXPOSE 8000

CMD ["bash", "-c", "bash /app/wait-for-model-download.sh && fastapi run main.py --port 8000"]
