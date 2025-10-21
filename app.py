from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import base64
from ultralytics import YOLO
import os
import io
from PIL import Image

app = Flask(__name__)

# Cargar el modelo YOLO entrenado
model = YOLO('modelo_entrenado/chaleco_detection/weights/best.pt')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/camera")
def camera_page():
    return render_template("camera.html")

@app.route("/detect", methods=["POST"])
def detect():
    try:
        data = request.get_json()
        image_data = data['image']
        
        # Decodificar imagen
        image_data = image_data.split(',')[1]
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convertir a OpenCV
        opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Detectar chalecos
        results = model(opencv_image, conf=0.5)
        annotated_image = results[0].plot()
        
        # Convertir resultado a base64
        _, buffer = cv2.imencode('.jpg', annotated_image)
        annotated_base64 = base64.b64encode(buffer).decode('utf-8')
        
        # Contar detecciones
        count = len(results[0].boxes) if results[0].boxes is not None else 0
        
        return jsonify({
            'success': True,
            'image': f"data:image/jpeg;base64,{annotated_base64}",
            'count': count
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)