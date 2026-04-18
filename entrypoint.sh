#!/bin/sh
echo "Esperando la base de datos..."
# ... (tu lógica de espera)
echo "Iniciando FastAPI..."
exec python -m uvicorn app.main:app --host 0.0.0.0 --port 8000