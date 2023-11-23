FROM python:3.9-slim

WORKDIR /app

RUN update-ca-certificates

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "./main.py"]
