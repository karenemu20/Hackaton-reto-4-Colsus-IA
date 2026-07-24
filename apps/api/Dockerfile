# Build context = raiz del repo (necesita contexts/, contracts/, plataforma/, context/data/)
FROM python:3.12-slim

WORKDIR /app

# Deps primero: mejor cache de capas
COPY apps/api/requirements.txt /app/apps/api/requirements.txt
RUN pip install --no-cache-dir -r apps/api/requirements.txt

# El repo entero: el api importa contexts.*, contracts.*, plataforma.* y lee context/data/*.csv
COPY . /app

EXPOSE 8000
CMD ["uvicorn", "apps.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
