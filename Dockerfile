FROM python:3.11-slim

WORKDIR /app

COPY /requirements.txt .
COPY /wait-for-model-download.sh .

RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y curl

COPY app/ .
COPY templates/ templates/

EXPOSE 8000

CMD ["./wait-for-model-download.sh" "&&", "fastapi", "run", "main.py", "--port", "8000"]

