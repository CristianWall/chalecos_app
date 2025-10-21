# 🦺 Sistema de Detección de Chalecos

Sistema web simple para detectar chalecos de seguridad en tiempo real usando YOLO.

## 🚀 Instalación y Uso

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Ejecutar la aplicación
```bash
python app.py
```

### 3. Abrir en el navegador
```
http://localhost:5000
```

## 📱 Uso

1. **Página Principal**: Haz clic en "Iniciar Detección"
2. **Cámara**: Permite acceso a la cámara web
3. **Detección**: Haz clic en "Detectar Chalecos" para análisis automático cada 2 segundos

## 🌐 Despliegue

### Heroku
```bash
heroku create tu-app-nombre
git add .
git commit -m "Deploy"
git push heroku main
```

### Railway
1. Conecta tu repositorio
2. Despliega automáticamente

## 📁 Archivos

- `app.py` - Aplicación Flask principal
- `templates/index.html` - Página principal
- `templates/camera.html` - Detección en tiempo real
- `modelo_entrenado/` - Modelo YOLO entrenado
- `requirements.txt` - Dependencias
- `Procfile` - Configuración para Heroku/Railway

## ✅ Características

- ✅ Detección en tiempo real con cámara web
- ✅ Modelo YOLO entrenado para chalecos
- ✅ Solo YOLO + PIL (sin OpenCV)
- ✅ Interfaz simple y fácil de usar
- ✅ Contador de chalecos detectados
- ✅ Despliegue fácil en la nube
