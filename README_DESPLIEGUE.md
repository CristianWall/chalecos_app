# 🚀 Guía de Despliegue en Heroku - Detección de Chalecos

## 📋 Resumen del Proyecto

Esta aplicación web permite detectar chalecos de seguridad en tiempo real usando:
- **Backend**: Flask + YOLO v8
- **Frontend**: HTML5 + JavaScript (acceso a cámara web)
- **Modelo**: YOLO entrenado específicamente para detectar chalecos
- **Plataforma**: Heroku (despliegue público)

## 🎯 Características

- ✅ Detección en tiempo real desde la cámara web
- ✅ Interfaz web moderna y responsive
- ✅ Acceso público desde cualquier dispositivo
- ✅ Modelo entrenado específicamente para chalecos de seguridad
- ✅ Despliegue automático en Heroku

## 📁 Estructura del Proyecto

```
despliegue/
├── app.py                 # Aplicación Flask principal
├── Procfile              # Configuración de Heroku
├── requirements.txt      # Dependencias de Python
├── runtime.txt           # Versión de Python
├── .gitignore           # Archivos a ignorar en Git
├── templates/
│   └── index.html       # Interfaz web
├── chaleco_detection/
│   └── weights/
│       └── best.pt      # Modelo YOLO entrenado
└── README_DESPLIEGUE.md # Esta guía
```

## 🚀 Pasos para Desplegar en Heroku

### 1. Preparación Inicial

**Asegúrate de tener:**
- ✅ Cuenta de Heroku creada
- ✅ Git instalado en tu computadora
- ✅ Heroku CLI instalado

### 2. Instalar Heroku CLI (si no lo tienes)

**Windows:**
```bash
# Descargar desde: https://devcenter.heroku.com/articles/heroku-cli
# O usar Chocolatey:
choco install heroku-cli
```

**Verificar instalación:**
```bash
heroku --version
```

### 3. Iniciar Sesión en Heroku

```bash
heroku login
```

### 4. Navegar a la Carpeta de Despliegue

```bash
cd despliegue
```

### 5. Inicializar Git (si no existe)

```bash
git init
```

### 6. Crear Aplicación en Heroku

```bash
heroku create tu-app-chalecos-detection
```
*Reemplaza "tu-app-chalecos-detection" con un nombre único para tu app*

### 7. Configurar Git para Heroku

```bash
git add .
git commit -m "Primera versión - Detección de chalecos"
git push heroku main
```

### 8. Verificar el Despliegue

```bash
heroku logs --tail
```

### 9. Abrir la Aplicación

```bash
heroku open
```

## 🔧 Comandos Útiles de Heroku

### Ver logs en tiempo real:
```bash
heroku logs --tail
```

### Ver información de la app:
```bash
heroku info
```

### Reiniciar la aplicación:
```bash
heroku restart
```

### Ver variables de entorno:
```bash
heroku config
```

### Abrir consola de Python:
```bash
heroku run python
```

## 🌐 Acceso a la Aplicación

Una vez desplegada, tu aplicación estará disponible en:
```
https://tu-app-chalecos-detection.herokuapp.com
```

## 🎮 Cómo Usar la Aplicación

1. **Abrir la aplicación** en cualquier navegador web
2. **Hacer clic en "Iniciar Cámara"** (permite acceso a la cámara)
3. **Posicionarse frente a la cámara**
4. **Hacer clic en "Capturar y Detectar"**
5. **Ver los resultados** de la detección

## 🔍 Funcionalidades de la App

### Detección de Chalecos:
- **sin_chaleco**: Persona sin chaleco de seguridad
- **con_chaleco**: Persona con chaleco de seguridad

### Información mostrada:
- ✅ Clase detectada
- ✅ Nivel de confianza (%)
- ✅ Bounding boxes en la imagen
- ✅ Estadísticas en tiempo real

## 🛠️ Solución de Problemas

### Error: "No se pudo acceder a la cámara"
- **Solución**: Asegúrate de permitir el acceso a la cámara en tu navegador
- **Chrome**: Configuración → Privacidad → Configuración del sitio → Cámara

### Error: "Modelo no cargado"
- **Solución**: Verifica que el archivo `best.pt` esté en la carpeta correcta
- **Comando**: `heroku logs --tail` para ver errores detallados

### La aplicación no responde
- **Solución**: Reinicia la aplicación
- **Comando**: `heroku restart`

### Error de memoria en Heroku
- **Solución**: Heroku tiene límites de memoria, considera usar un plan superior
- **Comando**: `heroku ps:scale web=1` (para verificar el estado)

## 📊 Monitoreo y Mantenimiento

### Ver estado de la aplicación:
```bash
heroku ps
```

### Ver uso de recursos:
```bash
heroku logs --tail
```

### Actualizar la aplicación:
```bash
git add .
git commit -m "Actualización de la aplicación"
git push heroku main
```

## 🔒 Seguridad

- ✅ La aplicación no almacena imágenes
- ✅ Las detecciones se procesan en tiempo real
- ✅ No se guardan datos personales
- ✅ Acceso seguro por HTTPS

## 🎯 Próximos Pasos

Después del despliegue exitoso, puedes:

1. **Compartir el enlace** con otros usuarios
2. **Integrar en sistemas existentes** usando la API
3. **Mejorar el modelo** con más datos de entrenamiento
4. **Añadir más funcionalidades** (detección múltiple, alertas, etc.)

## 📞 Soporte

Si tienes problemas con el despliegue:

1. **Revisa los logs**: `heroku logs --tail`
2. **Verifica la configuración**: `heroku config`
3. **Consulta la documentación de Heroku**: https://devcenter.heroku.com/

---

**¡Tu aplicación de detección de chalecos estará lista para usar en la web! 🌐**
