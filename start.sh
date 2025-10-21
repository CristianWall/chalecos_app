#!/bin/bash

# Script de inicio para Railway
echo "🚀 Iniciando aplicación..."

# Verificar variables de entorno de Railway
echo "📋 Variables de Railway:"
echo "   PORT: $PORT"
echo "   FLASK_ENV: $FLASK_ENV"
echo "   MODEL_PATH: $MODEL_PATH"
echo "   CONFIDENCE_THRESHOLD: $CONFIDENCE_THRESHOLD"
echo "   IOU_THRESHOLD: $IOU_THRESHOLD"

# Si PORT no está definido, usar 5000
if [ -z "$PORT" ]; then
    echo "⚠️ PORT no definido, usando 5000"
    export PORT=5000
fi

# Verificar que el modelo existe
if [ -n "$MODEL_PATH" ] && [ -f "$MODEL_PATH" ]; then
    echo "✅ Modelo encontrado en: $MODEL_PATH"
else
    echo "⚠️ Modelo no encontrado en: $MODEL_PATH"
fi

# Iniciar la aplicación
echo "✅ Iniciando en puerto $PORT"
exec gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --threads 4 --timeout 120 --access-logfile - --error-logfile -
