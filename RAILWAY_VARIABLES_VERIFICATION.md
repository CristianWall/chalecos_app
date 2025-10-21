# 🔧 Verificación de Variables de Railway

## ✅ Variables que Debes Tener Configuradas en Railway

### 1. Acceder a Variables en Railway
1. **Ve a tu proyecto en Railway**
2. **Haz clic en tu servicio** (la aplicación web)
3. **Ve a la pestaña "Variables"**
4. **Verifica que tengas estas variables:**

### 2. Variables Requeridas

| Variable | Valor | Descripción |
|----------|-------|-------------|
| `PORT` | `5000` | Puerto donde escucha la aplicación |
| `FLASK_ENV` | `production` | Entorno de producción |
| `MODEL_PATH` | `modelo_entrenado/chaleco_detection/weights/best.pt` | Ruta al modelo YOLO |
| `CONFIDENCE_THRESHOLD` | `0.5` | Umbral de confianza para detección |
| `IOU_THRESHOLD` | `0.45` | Umbral IoU para NMS |

### 3. Configuración del Healthcheck

En Railway Settings → Health Check:
- **Healthcheck Path:** `/health`
- **Healthcheck Timeout:** `300` segundos (5 minutos)

## 📊 Logs que Deberías Ver

### Logs Exitosos:
```
🚀 Iniciando aplicación...
📋 Variables de Railway:
   PORT: 5000
   FLASK_ENV: production
   MODEL_PATH: modelo_entrenado/chaleco_detection/weights/best.pt
   CONFIDENCE_THRESHOLD: 0.5
   IOU_THRESHOLD: 0.45
✅ Modelo encontrado en: modelo_entrenado/chaleco_detection/weights/best.pt
✅ Iniciando en puerto 5000
[INFO] Starting gunicorn 21.2.0
[INFO] Listening at: http://0.0.0.0:5000
🔧 Configuración:
   MODEL_PATH: modelo_entrenado/chaleco_detection/weights/best.pt
   CONFIDENCE_THRESHOLD: 0.5
   IOU_THRESHOLD: 0.45
   PORT: 5000
✅ Cargando modelo YOLO...
✅ Modelo cargado exitosamente
✅ Aplicación iniciada - Modelo cargando en background
```

### Healthcheck Exitoso:
```
GET /health HTTP/1.1" 200
{
  "status": "healthy",
  "timestamp": 1640995200.0,
  "model_loaded": true,
  "port": "5000",
  "model_path": "modelo_entrenado/chaleco_detection/weights/best.pt"
}
```

## 🚨 Problemas Comunes y Soluciones

### Problema 1: Variables No Definidas
**Error:** Variables no aparecen en los logs
**Solución:** 
1. Ve a Railway → Variables
2. Agrega cada variable manualmente
3. Haz clic en "Deploy" para aplicar cambios

### Problema 2: Modelo No Encontrado
**Error:** `⚠️ Modelo no encontrado en: [ruta]`
**Solución:**
1. Verifica que `MODEL_PATH` sea exactamente: `modelo_entrenado/chaleco_detection/weights/best.pt`
2. Asegúrate de que el archivo `best.pt` esté en esa ruta

### Problema 3: Healthcheck Fallando
**Error:** `Attempt #1 failed with service unavailable`
**Solución:**
1. Verifica que `PORT=5000` esté configurado
2. Aumenta el timeout del healthcheck a 300 segundos
3. Usa `/health` como path del healthcheck

## 🔍 Verificación Paso a Paso

### Paso 1: Verificar Variables
```bash
# En Railway Logs, busca:
📋 Variables de Railway:
   PORT: 5000
   FLASK_ENV: production
   MODEL_PATH: modelo_entrenado/chaleco_detection/weights/best.pt
```

### Paso 2: Verificar Modelo
```bash
# En Railway Logs, busca:
✅ Modelo encontrado en: modelo_entrenado/chaleco_detection/weights/best.pt
```

### Paso 3: Verificar Servidor
```bash
# En Railway Logs, busca:
[INFO] Starting gunicorn 21.2.0
[INFO] Listening at: http://0.0.0.0:5000
```

### Paso 4: Verificar Healthcheck
```bash
# En Railway Logs, busca:
GET /health HTTP/1.1" 200
```

## 🎯 Configuración Final Recomendada

### Variables en Railway:
```
PORT=5000
FLASK_ENV=production
MODEL_PATH=modelo_entrenado/chaleco_detection/weights/best.pt
CONFIDENCE_THRESHOLD=0.5
IOU_THRESHOLD=0.45
```

### Healthcheck en Railway:
- **Path:** `/health`
- **Timeout:** `300` segundos
- **Retries:** `3`

## 🚀 Para Aplicar Cambios

```bash
git add .
git commit -m "Fix: Usar variables de Railway configuradas en la plataforma"
git push origin main
```

## ✅ Resultado Esperado

Después de configurar las variables correctamente:

```
✅ Build successful
🚀 Iniciando aplicación...
📋 Variables de Railway: [todas las variables mostradas]
✅ Modelo encontrado en: [ruta correcta]
✅ Iniciando en puerto 5000
✅ Health check passed
✅ Service deployed
✅ Available at: https://tu-app.railway.app
```

**¡Con las variables correctamente configuradas en Railway, tu aplicación debería funcionar perfectamente!** 🎉
