"""
Aplicación Flask para detección de chalecos de seguridad en tiempo real
Desplegable en Heroku con acceso público
"""

import os
import cv2
import base64
import numpy as np
from flask import Flask, render_template, request, jsonify, Response
from ultralytics import YOLO
import io
from PIL import Image
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Variable global para el modelo
model = None

def load_model():
    """Carga el modelo YOLO entrenado"""
    global model
    try:
        # Buscar el modelo en diferentes ubicaciones
        model_paths = [
            "chaleco_detection/weights/best.pt",
            "modelo_entrenado/chaleco_detection/weights/best.pt",
            "best.pt"
        ]
        
        model_path = None
        for path in model_paths:
            if os.path.exists(path):
                model_path = path
                break
        
        if model_path:
            model = YOLO(model_path)
            logger.info(f"Modelo cargado desde: {model_path}")
        else:
            # Usar modelo pre-entrenado como fallback
            model = YOLO('yolov8n.pt')
            logger.warning("Usando modelo pre-entrenado genérico")
            
        return True
    except Exception as e:
        logger.error(f"Error al cargar el modelo: {e}")
        return False

def process_image(image_data):
    """Procesa una imagen y devuelve las detecciones"""
    try:
        # Decodificar imagen base64
        image_bytes = base64.b64decode(image_data.split(',')[1])
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convertir a numpy array
        frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        if model is None:
            return {"error": "Modelo no cargado"}
        
        # Realizar detección
        results = model(frame, verbose=False)
        
        # Procesar resultados
        detections = []
        if len(results[0].boxes) > 0:
            for box in results[0].boxes:
                confidence = float(box.conf[0])
                class_id = int(box.cls[0])
                
                # Obtener nombre de la clase
                class_names = ['sin_chaleco', 'con_chaleco']
                if hasattr(results[0], 'names'):
                    class_names = list(results[0].names.values())
                
                class_name = class_names[class_id] if class_id < len(class_names) else f"Clase {class_id}"
                
                # Obtener coordenadas del bounding box
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                
                detections.append({
                    "class": class_name,
                    "confidence": confidence,
                    "bbox": [int(x1), int(y1), int(x2), int(y2)]
                })
        
        # Dibujar resultados en la imagen
        annotated_frame = results[0].plot()
        
        # Convertir imagen anotada a base64
        _, buffer = cv2.imencode('.jpg', annotated_frame)
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
        
        result = process_image(data['image'])
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error en endpoint de detección: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/health')
def health():
    """Endpoint de salud para verificar que la aplicación funciona"""
    return jsonify({
        "status": "healthy",
        "model_loaded": model is not None,
        "message": "Aplicación funcionando correctamente"
    })

@app.route('/info')
def info():
    """Información sobre la aplicación"""
    return jsonify({
        "name": "Detección de Chalecos de Seguridad",
        "version": "1.0.0",
        "model_loaded": model is not None,
        "description": "Aplicación web para detectar chalecos de seguridad en tiempo real usando YOLO"
    })

if __name__ == '__main__':
    # Cargar modelo al iniciar
    if load_model():
        logger.info("Aplicación iniciada correctamente")
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port, debug=False)
    else:
        logger.error("No se pudo cargar el modelo. Aplicación no iniciada.")
