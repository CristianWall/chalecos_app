from flask import Flask, render_template, request, jsonify
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
        
        # Convertir a RGB si es necesario
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Detectar chalecos con YOLO
        results = model(image, conf=0.5)
        
        # Obtener imagen con detecciones
        annotated_image = results[0].plot()
        
        # Convertir resultado a base64
        img_buffer = io.BytesIO()
        annotated_image.save(img_buffer, format='JPEG', quality=85)
        annotated_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
        
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