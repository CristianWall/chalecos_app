# 🔧 Guía para Configurar Healthcheck en Railway

## ❌ Problema Actual
Railway está fallando en el healthcheck con "service unavailable" porque:
1. Está usando `/health` pero el servicio no responde correctamente
2. La configuración de healthcheck no está optimizada

## ✅ Solución Paso a Paso

### Paso 1: Actualizar el Código
```bash
git add .
git commit -m "Fix: Simplificar healthcheck para Railway"
git push origin main
```

### Paso 2: Configurar Healthcheck en Railway

#### Opción A: Configuración Manual (Recomendada)

1. **Ve a tu proyecto en Railway**
2. **Haz clic en tu servicio** (la aplicación)
3. **Ve a "Settings"** (configuraciones)
4. **Busca la sección "Healthcheck"**
5. **Configura:**
   - **Healthcheck Path:** `/health`
   - **Healthcheck Timeout:** `300` segundos (5 minutos)
   - **Deja los otros campos por defecto**

#### Opción B: Usar Variables de Entorno

En Railway, agrega estas variables de entorno:
```
RAILWAY_HEALTHCHECK_TIMEOUT_SEC=300
PORT=5000
```

### Paso 3: Verificar Variables de Entorno

Asegúrate de tener estas variables configuradas:
```
PORT=5000
FLASK_ENV=production
MODEL_PATH=modelo_entrenado/chaleco_detection/weights/best.pt
```

### Paso 4: Forzar Nuevo Despliegue

1. **En Railway, haz clic en "Deploy"**
2. **O cambia cualquier variable de entorno** para forzar redeploy
3. **Monitorea los logs** en tiempo real

## 🔍 Diagnóstico de Logs

### Logs que Deberías Ver (Exitosos):
```
✅ Cargando modelo YOLO...
✅ Modelo cargado exitosamente: modelo_entrenado/chaleco_detection/weights/best.pt
✅ Modelo verificado y funcionando
✅ Iniciando aplicación...
✅ Aplicación lista!
✅ [INFO] Starting gunicorn...
✅ [INFO] Listening at: http://0.0.0.0:5000
✅ GET /health HTTP/1.1" 200
```

### Logs de Error Comunes:
```
❌ Error: Modelo no encontrado en modelo_entrenado/chaleco_detection/weights/best.pt
❌ Error cargando modelo: [ModuleNotFoundError]
❌ Address already in use
❌ Permission denied
```

## 🛠️ Soluciones a Problemas Específicos

### Problema 1: "Modelo no encontrado"
**Solución:** Verifica que el archivo `best.pt` esté en la ruta correcta

### Problema 2: "Module not found"
**Solución:** Todas las dependencias están en `requirements.txt`, Railway las instalará automáticamente

### Problema 3: "Address already in use"
**Solución:** El Dockerfile ya maneja esto correctamente

### Problema 4: "Permission denied"
**Solución:** El Dockerfile usa un usuario no-root, esto ya está solucionado

## 🎯 Configuración Final Recomendada

### Variables de Entorno en Railway:
```
PORT=5000
FLASK_ENV=production
MODEL_PATH=modelo_entrenado/chaleco_detection/weights/best.pt
CONFIDENCE_THRESHOLD=0.5
IOU_THRESHOLD=0.45
RAILWAY_HEALTHCHECK_TIMEOUT_SEC=300
```

### Configuración de Healthcheck:
- **Path:** `/health`
- **Timeout:** `300 seconds` (5 minutos)
- **Retries:** `Por defecto`

## 📊 Monitoreo del Despliegue

### 1. Verificar Build
```
✅ Build successful
✅ Docker image created
```

### 2. Verificar Healthcheck
```
✅ Starting Healthcheck
✅ GET /health HTTP/1.1" 200
✅ Health check passed
```

### 3. Verificar Servicio
```
✅ Service deployed
✅ Available at: https://tu-app.railway.app
```

## 🚨 Si el Problema Persiste

### Opción 1: Deshabilitar Healthcheck Temporalmente
1. En Railway Settings, **deshabilita el healthcheck**
2. Despliega la aplicación
3. Una vez que funcione, **habilita el healthcheck** con configuración manual

### Opción 2: Usar Endpoint Diferente
Si `/health` sigue fallando, puedes configurar Railway para usar `/ping`:
- **Healthcheck Path:** `/ping`

### Opción 3: Verificar Recursos
Railway puede necesitar más recursos:
- **CPU:** Al menos 0.5 vCPU
- **RAM:** Al menos 512MB
- **Storage:** Al menos 1GB

## ✅ Verificación Final

Una vez configurado correctamente, deberías ver:

1. **Build exitoso** ✅
2. **Healthcheck exitoso** ✅
3. **Aplicación funcionando** ✅
4. **URL disponible** ✅

**Tu aplicación de detección de chalecos estará funcionando en:**
`https://tu-app.railway.app`

## 🎉 ¡Listo!

Con esta configuración, tu aplicación debería pasar el healthcheck y desplegarse correctamente en Railway. El endpoint `/health` ahora es simple y robusto, devolviendo "OK" cuando el modelo está cargado correctamente.
