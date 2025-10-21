#!/bin/bash

# Script de inicio para Railway
echo "🚀 Iniciando aplicación..."

# Verificar variables de entorno
echo "PORT: $PORT"
echo "FLASK_ENV: $FLASK_ENV"

# Si PORT no está definido, usar 5000
if [ -z "$PORT" ]; then
    echo "⚠️ PORT no definido, usando 5000"
    export PORT=5000
fi

# Iniciar la aplicación
echo "✅ Iniciando en puerto $PORT"
exec gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --threads 4 --timeout 120 --access-logfile - --error-logfile -
