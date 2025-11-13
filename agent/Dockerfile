# agent/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código-fonte do agent
COPY agent.py .

# Expor porta opcional (caso queira expor /metrics)
EXPOSE 8000

# Comando padrão: roda o agent
CMD ["python", "agent.py"]
