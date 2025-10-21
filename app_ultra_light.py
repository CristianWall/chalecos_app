#!/usr/bin/env python3
"""
Aplicación Flask ULTRA-LIGERA para detección de chalecos
Versión optimizada para Heroku (500MB máximo)
Sin YOLO - Solo detección por colores
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

def detect_chaleco_colors(image_data):
    """
    Detección ultra-ligera basada en colores para chalecos
    Sin YOLO para mantener el tamaño bajo 500MB
    """
    try:
        # Decodificar imagen base64
        image_bytes = base64.b64decode(image_data.split(',')[1])
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convertir a numpy array
        frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Redimensionar para procesamiento más rápido
        height, width = frame.shape[:2]
        if width > 800:
            scale = 800 / width
            new_width = 800
            new_height = int(height * scale)
            frame = cv2.resize(frame, (new_width, new_height))
        
        # Convertir a HSV para mejor detección de colores
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Rangos de color para chalecos (amarillo/naranja/verde fluorescente)
        # Amarillo
        lower_yellow = np.array([20, 100, 100])
        upper_yellow = np.array([30, 255, 255])
        
        # Naranja
        lower_orange = np.array([10, 100, 100])
        upper_orange = np.array([20, 255, 255])
        
        # Verde fluorescente
        lower_green = np.array([40, 100, 100])
        upper_green = np.array([80, 255, 255])
        
        # Crear máscaras
        mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
        mask_orange = cv2.inRange(hsv, lower_orange, upper_orange)
        mask_green = cv2.inRange(hsv, lower_green, upper_green)
        
        # Combinar todas las máscaras
        mask = cv2.bitwise_or(mask_yellow, mask_orange)
        mask = cv2.bitwise_or(mask, mask_green)
        
        # Operaciones morfológicas para limpiar la máscara
        kernel = np.ones((5,5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        
        # Encontrar contornos
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        detections = []
        result_frame = frame.copy()
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 500:  # Filtrar contornos muy pequeños
                x, y, w, h = cv2.boundingRect(contour)
                
                # Calcular confianza basada en área y proporción
                aspect_ratio = w / h
                confidence = min(area / 5000, 0.95)
                
                # Ajustar confianza según la forma (chalecos suelen ser rectangulares)
                if 0.3 < aspect_ratio < 3.0:  # Proporción razonable
                    confidence *= 1.2
                
                # Determinar si es chaleco o no
                class_name = "con_chaleco" if confidence > 0.4 else "sin_chaleco"
                
                detections.append({
                    "class": class_name,
                    "confidence": min(confidence, 0.95),
                    "bbox": [x, y, x+w, y+h]
                })
                
                # Dibujar resultado
                color = (0, 255, 0) if class_name == "con_chaleco" else (0, 0, 255)
                cv2.rectangle(result_frame, (x, y), (x+w, y+h), color, 2)
                cv2.putText(result_frame, f"{class_name}: {confidence:.2f}", 
                           (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        # Si no hay detecciones, asumir sin chaleco
        if not detections:
            detections.append({
                "class": "sin_chaleco",
                "confidence": 0.6,
                "bbox": [0, 0, frame.shape[1], frame.shape[0]]
            })
            # Dibujar mensaje
            cv2.putText(result_frame, "Sin chaleco detectado", 
                       (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        # Convertir imagen resultado a base64
        _, buffer = cv2.imencode('.jpg', result_frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
        annotated_image = base64.b64encode(buffer).decode('utf-8')
        
        return {
            "detections": detections,
            "annotated_image": f"data:image/jpeg;base64,{annotated_image}",
            "success": True,
            "method": "color_detection"
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
        
        result = detect_chaleco_colors(data['image'])
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
        "message": "Aplicación ultra-ligera funcionando correctamente"
    })

@app.route('/info')
def info():
    """Información sobre la aplicación"""
    return jsonify({
        "name": "Detección de Chalecos Ultra-Ligera",
        "version": "1.0.0-ultra-light",
        "model_loaded": True,
        "description": "Aplicación web ultra-ligera para detectar chalecos usando detección de colores",
        "size": "< 500MB"
    })

if __name__ == '__main__':
    logger.info("Aplicación ultra-ligera iniciada - < 500MB")
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
