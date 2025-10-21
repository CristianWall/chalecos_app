# 🔍 Detector de Chalecos - Aplicación Web

Aplicación web en tiempo real para detectar chalecos de seguridad usando YOLOv8, optimizada para despliegue en Railway.

## 🚀 Características

- **Detección en tiempo real** usando la cámara web
- **Interfaz moderna y responsiva** con HTML5/CSS3/JavaScript
- **Modelo YOLOv8 optimizado** para mejor rendimiento
- **API REST** para integración con otros sistemas
- **Optimizado para Railway** con límite de 4GB

## 📋 Requisitos del Sistema

- Python 3.9+
- Cámara web
- Navegador moderno (Chrome, Firefox, Safari, Edge)
- 4GB de almacenamiento disponible (Railway)

## 🛠️ Instalación Local

1. **Clonar el repositorio:**
```bash
git clone <tu-repositorio>
cd despliegue
```

2. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

3. **Ejecutar la aplicación:**
```bash
python app.py
```

4. **Abrir en el navegador:**
```
http://localhost:5000
```

## 🚂 Despliegue en Railway

### Opción 1: Despliegue desde GitHub

1. **Subir código a GitHub:**
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <tu-repositorio-github>
git push -u origin main
```

2. **Conectar con Railway:**
   - Ve a [Railway.app](https://railway.app)
   - Crea una cuenta o inicia sesión
   - Haz clic en "New Project"
   - Selecciona "Deploy from GitHub repo"
   - Conecta tu repositorio de GitHub
   - Railway detectará automáticamente la configuración

3. **Configurar variables de entorno (opcional):**
```env
PORT=5000
MODEL_PATH=modelo_entrenado/chaleco_detection/weights/best.pt
CONFIDENCE_THRESHOLD=0.5
IOU_THRESHOLD=0.45
```

### Opción 2: Despliegue con Railway CLI

1. **Instalar Railway CLI:**
```bash
npm install -g @railway/cli
```

2. **Iniciar sesión:**
```bash
railway login
```

3. **Desplegar:**
```bash
railway init
railway up
```

## 📁 Estructura del Proyecto

```
despliegue/
├── app.py                          # Aplicación Flask principal
├── requirements.txt                 # Dependencias Python
├── runtime.txt                     # Versión de Python
├── Procfile                        # Comando de inicio para Railway
├── railway.json                    # Configuración específica de Railway
├── nixpacks.toml                   # Configuración de build
├── optimize_model.py               # Script de optimización del modelo
├── env.example                     # Variables de entorno de ejemplo
├── .gitignore                      # Archivos a ignorar en Git
├── README.md                       # Este archivo
├── templates/
│   └── index.html                  # Interfaz web
└── modelo_entrenado/
    └── chaleco_detection/
        └── weights/
            └── best.pt             # Modelo YOLOv8 entrenado
```

## 🔧 Configuración

### Variables de Entorno

| Variable | Descripción | Valor por Defecto |
|----------|-------------|-------------------|
| `PORT` | Puerto del servidor | 5000 |
| `MODEL_PATH` | Ruta al modelo | modelo_entrenado/chaleco_detection/weights/best.pt |
| `CONFIDENCE_THRESHOLD` | Umbral de confianza | 0.5 |
| `IOU_THRESHOLD` | Umbral IoU para NMS | 0.45 |

### Personalización del Modelo

Para usar tu propio modelo entrenado:

1. Coloca tu modelo en `modelo_entrenado/chaleco_detection/weights/best.pt`
2. Ajusta las clases en `app.py` si es necesario
3. Ejecuta `python optimize_model.py` para optimizar

## 📊 API Endpoints

### `GET /`
Página principal con la interfaz web.

### `POST /detect`
Detecta chalecos en una imagen.

**Request:**
```json
{
  "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ..."
}
```

**Response:**
```json
{
  "detections": [
    {
      "bbox": [100, 150, 200, 300],
      "confidence": 0.85,
      "class": "con_chaleco",
      "class_id": 1
    }
  ],
  "count": 1,
  "has_vest": true,
  "timestamp": 1640995200.0
}
```

### `GET /health`
Endpoint de salud para Railway.

**Response:**
```json
{
  "status": "healthy",
  "model_status": "loaded",
  "timestamp": 1640995200.0
}
```

### `GET /model_info`
Información del modelo cargado.

**Response:**
```json
{
  "model_path": "modelo_entrenado/chaleco_detection/weights/best.pt",
  "classes": ["sin_chaleco", "con_chaleco"],
  "confidence_threshold": 0.5,
  "iou_threshold": 0.45
}
```

## 🎯 Uso de la Aplicación

1. **Iniciar la cámara:** Haz clic en "Iniciar Cámara" y permite el acceso
2. **Detectar chalecos:** Haz clic en "Detectar Chalecos" para comenzar la detección automática
3. **Ver resultados:** La aplicación mostrará:
   - Estado en tiempo real (chaleco detectado/no detectado)
   - Información detallada de cada detección
   - Estadísticas acumuladas
4. **Detener:** Haz clic en "Detener" para parar la detección

## 🔍 Optimizaciones Implementadas

### Para Railway (4GB límite):
- **Modelo optimizado:** Solo se incluye el modelo `best.pt` necesario
- **Dependencias mínimas:** Versiones específicas para reducir tamaño
- **Imágenes sin cabeza:** `opencv-python-headless` para OpenCV
- **Configuración de workers:** 1 worker, 4 threads para Railway
- **Timeout configurado:** 120 segundos para procesamiento

### Para Rendimiento:
- **Detección asíncrona:** No bloquea la interfaz
- **Compresión de imágenes:** JPEG con calidad 0.8
- **Cache del modelo:** Se carga una sola vez
- **Threading seguro:** Uso de locks para el modelo

## 🐛 Solución de Problemas

### Error: "No se pudo acceder a la cámara"
- Verifica que la cámara no esté siendo usada por otra aplicación
- Asegúrate de permitir el acceso a la cámara en el navegador
- Prueba en modo HTTPS (Railway lo proporciona automáticamente)

### Error: "Modelo no cargado"
- Verifica que el archivo `best.pt` esté presente
- Comprueba los logs de Railway para errores de carga
- El modelo se carga automáticamente al iniciar la aplicación

### Rendimiento lento
- Reduce la resolución de la cámara
- Aumenta el intervalo de detección (actualmente 2 segundos)
- Verifica que Railway tenga suficientes recursos asignados

## 📈 Monitoreo en Railway

Railway proporciona métricas automáticas:
- **CPU Usage:** Monitoreo del uso de CPU
- **Memory Usage:** Seguimiento del uso de memoria
- **Network:** Tráfico de red
- **Logs:** Logs en tiempo real de la aplicación

## 🔒 Seguridad

- **HTTPS automático:** Railway proporciona SSL automático
- **Validación de entrada:** Se valida la imagen antes del procesamiento
- **Timeouts:** Configurados para evitar bloqueos
- **Error handling:** Manejo robusto de errores

## 📞 Soporte

Si encuentras problemas:
1. Revisa los logs en Railway
2. Verifica la configuración de variables de entorno
3. Asegúrate de que el modelo esté correctamente ubicado
4. Consulta la documentación de Railway

## 🚀 Próximas Mejoras

- [ ] Soporte para múltiples modelos
- [ ] Historial de detecciones
- [ ] Exportación de resultados
- [ ] API para batch processing
- [ ] Integración con bases de datos
- [ ] Notificaciones en tiempo real

---

**¡Tu aplicación está lista para detectar chalecos en tiempo real! 🎉**
