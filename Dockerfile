FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y curl
RUN curl -fsSL https://ollama.com/install.sh | sh

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000 5001 11434

CMD ["python3", "api_server.py"]
