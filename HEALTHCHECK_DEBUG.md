# 🔧 Debug del Healthcheck en Railway

## ❌ Problema Actual
El healthcheck sigue fallando después del build exitoso:
```
Attempt #1 failed with service unavailable. Continuing to retry for 4m54s
```

## ✅ Soluciones Implementadas

### 1. Endpoint `/health` Simplificado
```python
@app.route('/health')
def health():
    """Endpoint de salud para Railway - Simplificado"""
    return "OK", 200
```

### 2. Carga del Modelo Lazy
- El modelo se carga solo cuando se necesita
- No bloquea el inicio de la aplicación
- La app responde inmediatamente al healthcheck

### 3. Endpoints de Test
- `/ping` - Endpoint simple
- `/test` - Endpoint con información detallada
- `/health` - Healthcheck principal

## 🚀 Para Aplicar la Solución

```bash
git add .
git commit -m "Fix: Simplificar healthcheck para Railway"
git push origin main
```

## 📊 Logs Esperados

### Logs de Inicio:
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
Aplicación iniciada - Lista para recibir requests
```

### Healthcheck Exitoso:
```
GET /health HTTP/1.1" 200
```

## 🔍 Debugging en Railway

### 1. Verificar Logs de Inicio
En Railway Logs, busca:
```
✅ Iniciando en puerto 5000
[INFO] Starting gunicorn 21.2.0
[INFO] Listening at: http://0.0.0.0:5000
```

### 2. Verificar Variables
```
📋 Variables de Railway:
   PORT: 5000
   MODEL_PATH: modelo_entrenado/chaleco_detection/weights/best.pt
```

### 3. Verificar Healthcheck
```
GET /health HTTP/1.1" 200
```

## 🚨 Problemas Comunes

### Problema 1: Puerto Incorrecto
**Error:** App no escucha en el puerto correcto
**Solución:** Verificar que `PORT=5000` esté configurado

### Problema 2: Modelo No Encontrado
**Error:** `⚠️ Modelo no encontrado`
**Solución:** Verificar que `MODEL_PATH` sea correcto

### Problema 3: Variables No Definidas
**Error:** Variables no aparecen en logs
**Solución:** Configurar variables en Railway

## 🎯 Configuración Final

### Variables en Railway:
```
PORT=5000
FLASK_ENV=production
MODEL_PATH=modelo_entrenado/chaleco_detection/weights/best.pt
CONFIDENCE_THRESHOLD=0.5
IOU_THRESHOLD=0.45
RAILWAY_HEALTHCHECK_TIMEOUT_SEC=300
```

### Healthcheck en Railway:
- **Path:** `/health`
- **Timeout:** `300` segundos

## ✅ Resultado Esperado

Después de aplicar estos cambios:

```
✅ Build successful
🚀 Iniciando aplicación...
📋 Variables de Railway: [todas las variables]
✅ Modelo encontrado en: [ruta correcta]
✅ Iniciando en puerto 5000
[INFO] Starting gunicorn 21.2.0
[INFO] Listening at: http://0.0.0.0:5000
✅ Starting Healthcheck
✅ GET /health HTTP/1.1" 200
✅ Health check passed
✅ Service deployed
```

## 🔧 Endpoints Disponibles

- `/health` - Healthcheck principal (simplificado)
- `/ping` - Test simple
- `/test` - Test con información detallada
- `/` - Página principal
- `/detect` - Detección de chalecos

**¡Con estos cambios, el healthcheck debería pasar correctamente!** 🎉
