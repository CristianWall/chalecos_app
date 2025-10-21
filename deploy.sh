#!/bin/bash

# Script de despliegue rápido para Railway
# Ejecutar con: bash deploy.sh

echo "🚀 Iniciando despliegue para Railway..."

# Verificar que estamos en el directorio correcto
if [ ! -f "app.py" ]; then
    echo "❌ Error: No se encontró app.py. Ejecuta este script desde la carpeta despliegue/"
    exit 1
fi

# Verificar que el modelo existe
if [ ! -f "modelo_entrenado/chaleco_detection/weights/best.pt" ]; then
    echo "❌ Error: No se encontró el modelo best.pt"
    echo "Asegúrate de copiar el modelo desde ../modelo_entrenado/chaleco_detection/weights/best.pt"
    exit 1
fi

echo "✅ Verificaciones completadas"

# Inicializar Git si no existe
if [ ! -d ".git" ]; then
    echo "📦 Inicializando repositorio Git..."
    git init
    git branch -M main
fi

# Agregar todos los archivos
echo "📁 Agregando archivos al repositorio..."
git add .

# Commit inicial
echo "💾 Creando commit..."
git commit -m "🚀 Deploy: Aplicación de detección de chalecos para Railway"

echo ""
echo "🎉 ¡Preparación completada!"
echo ""
echo "📋 Próximos pasos para desplegar en Railway:"
echo ""
echo "1. 🔗 Subir a GitHub:"
echo "   git remote add origin <tu-repositorio-github>"
echo "   git push -u origin main"
echo ""
echo "2. 🚂 Conectar con Railway:"
echo "   - Ve a https://railway.app"
echo "   - Crea una cuenta o inicia sesión"
echo "   - Haz clic en 'New Project'"
echo "   - Selecciona 'Deploy from GitHub repo'"
echo "   - Conecta tu repositorio"
echo ""
echo "3. ⚙️ Configurar variables de entorno (opcional):"
echo "   - PORT=5000"
echo "   - MODEL_PATH=modelo_entrenado/chaleco_detection/weights/best.pt"
echo "   - CONFIDENCE_THRESHOLD=0.5"
echo "   - IOU_THRESHOLD=0.45"
echo ""
echo "4. 🚀 ¡Desplegar!"
echo "   Railway detectará automáticamente la configuración y desplegará tu app"
echo ""
echo "📖 Para más información, consulta README.md"
echo ""
echo "🎯 Tu aplicación estará disponible en: https://tu-app.railway.app"
