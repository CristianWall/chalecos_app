# 🔧 Solución al Error de Healthcheck en Railway

## ❌ Error Encontrado
```
1/1 replicas never became healthy!
Healthcheck failed!
```

## ✅ Soluciones Implementadas

### 1. Endpoint de Healthcheck Mejorado

He agregado un endpoint `/ping` más simple y robusto:

```python
@app.route('/ping')
def ping():
    """Endpoint simple de ping para healthcheck"""
    return "pong", 200
```

### 2. Configuración de Railway Actualizada

Cambié la configuración para usar `/ping` en lugar de `/health`:

```json
{
  "healthcheckPath": "/ping",
  "healthcheckTimeout": 60,
  "restartPolicyMaxRetries": 5
}
```

### 3. Dockerfile Mejorado

Agregué logs para mejor debugging:

```dockerfile
CMD gunicorn app:app --bind 0.0.0.0:${PORT:-5000} --workers 1 --threads 4 --timeout 120 --access-logfile - --error-logfile -
```

## 🚀 Pasos para Solucionar

### Paso 1: Actualizar el Código
```bash
git add .
git commit -m "Fix: Mejorar healthcheck para Railway"
git push origin main
```

### Paso 2: En la App de Railway

1. **Ve a tu proyecto en Railway**
2. **Haz clic en "Deploy"** para forzar un nuevo despliegue
3. **Monitorea los logs** en tiempo real

### Paso 3: Verificar Variables de Entorno

En Railway, asegúrate de tener estas variables:
```
PORT=5000
FLASK_ENV=production
```

### Paso 4: Configurar Healthcheck Manualmente

Si el problema persiste, puedes configurar el healthcheck manualmente:

1. **Ve a "Settings"** en tu proyecto Railway
2. **Busca "Health Check"**
3. **Configura:**
   - **Path:** `/ping`
   - **Timeout:** `60 seconds`
   - **Interval:** `30 seconds`

## 🔍 Diagnóstico

### Probar Localmente
Ejecuta el script de diagnóstico:
```bash
python test_local.py
```

### Verificar Logs en Railway
1. Ve a tu proyecto en Railway
2. Haz clic en "Logs"
3. Busca errores como:
   - "Address already in use"
   - "Module not found"
   - "Permission denied"

### Endpoints Disponibles
- `/ping` - Healthcheck simple
- `/health` - Healthcheck detallado
- `/` - Página principal
- `/model_info` - Información del modelo

## 🐛 Problemas Comunes y Soluciones

### 1. Puerto Incorrecto
**Error:** `Address already in use`
**Solución:** Asegúrate de usar `$PORT` en el comando de inicio

### 2. Modelo No Encontrado
**Error:** `Model not loaded`
**Solución:** Verifica que `best.pt` esté en la ruta correcta

### 3. Permisos
**Error:** `Permission denied`
**Solución:** El Dockerfile ya maneja esto con usuario no-root

### 4. Dependencias Faltantes
**Error:** `Module not found`
**Solución:** Verifica que todas las dependencias estén en `requirements.txt`

## 📊 Monitoreo

### Logs Importantes a Revisar
```bash
# En Railway Logs, busca:
✅ "Iniciando aplicación..."
✅ "Modelo cargado exitosamente"
✅ "Aplicación lista!"
✅ "GET /ping HTTP/1.1" 200
```

### Métricas de Salud
- **CPU Usage:** Debería estar < 50%
- **Memory Usage:** Debería estar < 1GB
- **Response Time:** Debería ser < 2 segundos

## 🎯 Configuración Final Recomendada

### Variables de Entorno en Railway
```
PORT=5000
FLASK_ENV=production
MODEL_PATH=modelo_entrenado/chaleco_detection/weights/best.pt
CONFIDENCE_THRESHOLD=0.5
IOU_THRESHOLD=0.45
```

### Configuración de Healthcheck
- **Path:** `/ping`
- **Timeout:** `60 seconds`
- **Interval:** `30 seconds`
- **Retries:** `3`

## 🚨 Si el Problema Persiste

### Opción 1: Deshabilitar Healthcheck Temporalmente
En Railway Settings, deshabilita el healthcheck y usa solo el despliegue básico.

### Opción 2: Usar Railway CLI
```bash
railway login
railway link
railway up
```

### Opción 3: Verificar Recursos
Railway puede necesitar más recursos:
- **CPU:** Al menos 0.5 vCPU
- **RAM:** Al menos 512MB
- **Storage:** Al menos 1GB

## ✅ Verificación Final

Una vez que el healthcheck pase, deberías ver:
```
✅ Deployment successful
✅ Health check passed
✅ Application running on https://tu-app.railway.app
```

¡Tu aplicación de detección de chalecos estará funcionando! 🎉
