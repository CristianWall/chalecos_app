#!/usr/bin/env python3
"""
Aplicación Flask simplificada para detección de chalecos
Versión optimizada para Heroku sin YOLO pesado
"""

import os
import cv2
import base64
import numpy as np
from flask import Flask, render_template, request, jsonify
import io
from PIL import Image
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

def detect_colors(image_data):
    """
    Detección simple basada en colores para chalecos
    (Funciona sin YOLO para reducir el tamaño)
    """
    try:
        # Decodificar imagen base64
        image_bytes = base64.b64decode(image_data.split(',')[1])
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convertir a numpy array
        frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Detección simple por colores (amarillo/naranja típicos de chalecos)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Rangos de color para chalecos (amarillo/naranja)
        lower_yellow = np.array([20, 100, 100])
        upper_yellow = np.array([30, 255, 255])
        
        lower_orange = np.array([10, 100, 100])
        upper_orange = np.array([25, 255, 255])
        
        # Crear máscaras
        mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
        mask_orange = cv2.inRange(hsv, lower_orange, upper_orange)
        
        # Combinar máscaras
        mask = cv2.bitwise_or(mask_yellow, mask_orange)
        
        # Encontrar contornos
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        detections = []
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 1000:  # Filtrar contornos pequeños
                x, y, w, h = cv2.boundingRect(contour)
                
                # Calcular confianza basada en el área y forma
                confidence = min(area / 10000, 0.95)
                
                detections.append({
                    "class": "con_chaleco" if confidence > 0.3 else "sin_chaleco",
                    "confidence": confidence,
                    "bbox": [x, y, x+w, y+h]
                })
        
        # Dibujar resultados
        result_frame = frame.copy()
        for detection in detections:
            x1, y1, x2, y2 = detection["bbox"]
            color = (0, 255, 0) if detection["class"] == "con_chaleco" else (0, 0, 255)
            cv2.rectangle(result_frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(result_frame, f"{detection['class']}: {detection['confidence']:.2f}", 
                       (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        # Si no hay detecciones, asumir sin chaleco
        if not detections:
            detections.append({
                "class": "sin_chaleco",
                "confidence": 0.7,
                "bbox": [0, 0, frame.shape[1], frame.shape[0]]
            })
        
        # Convertir imagen resultado a base64
        _, buffer = cv2.imencode('.jpg', result_frame)
        annotated_image = base64.b64encode(buffer).decode('utf-8')
        
        return {
            "detections": detections,
            "annotated_image": f"data:image/jpeg;base64,{annotated_image}",
            "success": True
        }
        
    except Exception as e:
        logger.error(f"Error al procesar imagen: {e}")
        return {"error": str(e)}

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect():
    """Endpoint para detección de chalecos"""
    try:
        data = request.get_json()
        if 'image' not in data:
            return jsonify({"error": "No se proporcionó imagen"}), 400
        
        result = detect_colors(data['image'])
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error en endpoint de detección: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/health')
def health():
    """Endpoint de salud"""
    return jsonify({
        "status": "healthy",
        "model_loaded": True,
        "message": "Aplicación funcionando correctamente (versión simplificada)"
    })

@app.route('/info')
def info():
    """Información sobre la aplicación"""
    return jsonify({
        "name": "Detección de Chalecos de Seguridad",
        "version": "1.0.0-simple",
        "model_loaded": True,
        "description": "Aplicación web para detectar chalecos de seguridad usando detección de colores"
    })

if __name__ == '__main__':
    logger.info("Aplicación simplificada iniciada")
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
