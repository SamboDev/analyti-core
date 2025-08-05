FROM python:3.11-slim

WORKDIR /app

# Copia los archivos de dependencias primero (mejor para el cache)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código
COPY . .

# Expone el puerto 8001 para FastAPI
EXPOSE 8001

# Comando para levantar el servidor FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]

