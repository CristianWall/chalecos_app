# 🔧 Configurar Variables de Entorno en Railway

## 📱 Cómo Configurar Variables en Railway

### Paso 1: Acceder a tu Proyecto
1. **Ve a [Railway.app](https://railway.app)**
2. **Inicia sesión** en tu cuenta
3. **Haz clic en tu proyecto** (el que tiene tu app de detección de chalecos)

### Paso 2: Acceder a Variables de Entorno
1. **Haz clic en tu servicio** (la aplicación web)
2. **Ve a la pestaña "Variables"** (está en el menú superior)
3. **O ve a "Settings" → "Variables"**

### Paso 3: Agregar Variables de Entorno

#### Variables Esenciales:
```
PORT=5000
FLASK_ENV=production
MODEL_PATH=modelo_entrenado/chaleco_detection/weights/best.pt
CONFIDENCE_THRESHOLD=0.5
IOU_THRESHOLD=0.45
RAILWAY_HEALTHCHECK_TIMEOUT_SEC=300
```

#### Cómo Agregar Cada Variable:

1. **Haz clic en "New Variable"** o el botón "+"
2. **Nombre:** `PORT`
   **Valor:** `5000`
   **Haz clic en "Add"**

3. **Haz clic en "New Variable"** otra vez
4. **Nombre:** `FLASK_ENV`
   **Valor:** `production`
   **Haz clic en "Add"**

5. **Haz clic en "New Variable"**
6. **Nombre:** `MODEL_PATH`
   **Valor:** `modelo_entrenado/chaleco_detection/weights/best.pt`
   **Haz clic en "Add"**

7. **Haz clic en "New Variable"**
8. **Nombre:** `CONFIDENCE_THRESHOLD`
   **Valor:** `0.5`
   **Haz clic en "Add"**

9. **Haz clic en "New Variable"**
10. **Nombre:** `IOU_THRESHOLD`
    **Valor:** `0.45`
    **Haz clic en "Add"**

11. **Haz clic en "New Variable"**
12. **Nombre:** `RAILWAY_HEALTHCHECK_TIMEOUT_SEC`
    **Valor:** `300`
    **Haz clic en "Add"**

### Paso 4: Configurar Healthcheck

#### Opción A: En Variables (Recomendada)
Ya agregaste `RAILWAY_HEALTHCHECK_TIMEOUT_SEC=300`

#### Opción B: En Settings
1. **Ve a "Settings"**
2. **Busca "Health Check"**
3. **Healthcheck Path:** `/health`
4. **Healthcheck Timeout:** `300` segundos

### Paso 5: Forzar Nuevo Despliegue
1. **Después de agregar todas las variables, haz clic en "Deploy"**
2. **O cambia cualquier variable** para forzar redeploy
3. **Monitorea los logs** en tiempo real

## 🎯 Variables Explicadas

| Variable | Propósito | Valor |
|----------|-----------|-------|
| `PORT` | Puerto donde escucha la app | `5000` |
| `FLASK_ENV` | Entorno de producción | `production` |
| `MODEL_PATH` | Ruta al modelo YOLO | `modelo_entrenado/chaleco_detection/weights/best.pt` |
| `CONFIDENCE_THRESHOLD` | Umbral de confianza | `0.5` |
| `IOU_THRESHOLD` | Umbral IoU para NMS | `0.45` |
| `RAILWAY_HEALTHCHECK_TIMEOUT_SEC` | Timeout del healthcheck | `300` |

## 📊 Verificación

### Después de Configurar las Variables:

1. **Ve a "Logs"** en Railway
2. **Busca estos mensajes:**
   ```
   ✅ PORT=5000
   ✅ FLASK_ENV=production
   ✅ MODEL_PATH=modelo_entrenado/chaleco_detection/weights/best.pt
   ✅ Cargando modelo YOLO...
   ✅ Modelo cargado exitosamente
   ✅ GET /health HTTP/1.1" 200
   ✅ Health check passed
   ```

### Si Aparecen Errores:
```
❌ Error: Modelo no encontrado
❌ ModuleNotFoundError
❌ Address already in use
```

## 🚨 Solución a "Service Unavailable"

El error "service unavailable" significa que:
1. **La aplicación no está escuchando en el puerto correcto**
2. **El modelo no se está cargando**
3. **Hay un error en el código**

### Con las Variables Configuradas:
- `PORT=5000` → La app escuchará en el puerto correcto
- `MODEL_PATH=...` → La app encontrará el modelo
- `RAILWAY_HEALTHCHECK_TIMEOUT_SEC=300` → 5 minutos para cargar

## ✅ Resultado Esperado

Después de configurar las variables y hacer redeploy:

```
✅ Build successful
✅ Starting Healthcheck
✅ Attempt #1: GET /health HTTP/1.1" 200
✅ Health check passed
✅ Service deployed
✅ Available at: https://tu-app.railway.app
```

## 🎉 ¡Listo!

Con estas variables configuradas, tu aplicación debería:
1. **Cargar el modelo correctamente**
2. **Escuchar en el puerto correcto**
3. **Pasar el healthcheck**
4. **Desplegarse exitosamente**

**¡Tu aplicación de detección de chalecos estará funcionando!** 🚀
