#!/usr/bin/env python3
"""
Aplicación Flask para detección de chalecos en tiempo real
Optimizada para despliegue en Railway
"""

import os
import cv2
import base64
import numpy as np
from flask import Flask, render_template, request, jsonify, Response
from ultralytics import YOLO
import io
from PIL import Image
import threading
import time

app = Flask(__name__)

# Configuración
MODEL_PATH = "modelo_entrenado/chaleco_detection/weights/best.pt"
CONFIDENCE_THRESHOLD = 0.5
IOU_THRESHOLD = 0.45

# Variables globales
model = None
model_lock = threading.Lock()

def load_model():
    """Cargar el modelo YOLO de forma segura"""
    global model
    try:
        with model_lock:
            if model is None:
                print("Cargando modelo YOLO...")
                model = YOLO(MODEL_PATH)
                print(f"Modelo cargado exitosamente: {MODEL_PATH}")
        return True
    except Exception as e:
        print(f"Error cargando modelo: {e}")
        return False

def preprocess_image(image_data):
    """Preprocesar imagen para detección"""
    try:
        # Decodificar imagen base64
        image_bytes = base64.b64decode(image_data.split(',')[1])
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convertir a RGB si es necesario
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Convertir a numpy array
        image_np = np.array(image)
        
        return image_np
    except Exception as e:
        print(f"Error preprocesando imagen: {e}")
        return None

def detect_chalecos(image_np):
    """Detectar chalecos en la imagen"""
    try:
        if model is None:
            return None, "Modelo no cargado"
        
        # Realizar detección
        results = model(image_np, conf=CONFIDENCE_THRESHOLD, iou=IOU_THRESHOLD)
        
        detections = []
        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for box in boxes:
                    # Obtener coordenadas y confianza
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    confidence = box.conf[0].cpu().numpy()
                    class_id = int(box.cls[0].cpu().numpy())
                    
                    # Mapear class_id a nombre de clase
                    class_names = model.names
                    class_name = class_names[class_id] if class_id in class_names else f"clase_{class_id}"
                    
                    detections.append({
                        'bbox': [int(x1), int(y1), int(x2), int(y2)],
                        'confidence': float(confidence),
                        'class': class_name,
                        'class_id': class_id
                    })
        
        return detections, None
    except Exception as e:
        print(f"Error en detección: {e}")
        return None, str(e)

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect():
    """Endpoint para detección de chalecos"""
    try:
        data = request.get_json()
        if not data or 'image' not in data:
            return jsonify({'error': 'No se proporcionó imagen'}), 400
        
        # Preprocesar imagen
        image_np = preprocess_image(data['image'])
        if image_np is None:
            return jsonify({'error': 'Error procesando imagen'}), 400
        
        # Detectar chalecos
        detections, error = detect_chalecos(image_np)
        if error:
            return jsonify({'error': error}), 500
        
        # Preparar respuesta
        response = {
            'detections': detections,
            'count': len(detections),
            'timestamp': time.time()
        }
        
        # Determinar si hay chalecos detectados
        chalecos_detectados = any(det['class'] == 'con_chaleco' for det in detections)
        response['has_vest'] = chalecos_detectados
        
        return jsonify(response)
    
    except Exception as e:
        print(f"Error en endpoint detect: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@app.route('/health')
def health():
    """Endpoint de salud para Railway"""
    try:
        model_status = "loaded" if model is not None else "not_loaded"
        return jsonify({
            'status': 'healthy',
            'model_status': model_status,
            'timestamp': time.time()
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': time.time()
        }), 500

@app.route('/')
def index():
    """Página principal"""
    try:
        return render_template('index.html')
    except Exception as e:
        return f"Error loading template: {str(e)}", 500

@app.route('/ping')
def ping():
    """Endpoint simple de ping para healthcheck"""
    return "pong", 200

@app.route('/model_info')
def model_info():
    """Información del modelo"""
    if model is None:
        return jsonify({'error': 'Modelo no cargado'}), 500
    
    try:
        return jsonify({
            'model_path': MODEL_PATH,
            'classes': list(model.names.values()),
            'confidence_threshold': CONFIDENCE_THRESHOLD,
            'iou_threshold': IOU_THRESHOLD
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Cargar modelo al iniciar la aplicación
print("Iniciando aplicación...")
if load_model():
    print("Aplicación lista!")
else:
    print("Error: No se pudo cargar el modelo")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
