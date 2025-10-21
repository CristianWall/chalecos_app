#!/usr/bin/env python3
"""
Aplicación Flask ultra-simplificada para Railway
"""

from flask import Flask, render_template, request, jsonify
import os
import time

app = Flask(__name__)

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/health')
def health():
    """Endpoint de salud para Railway"""
    return "OK", 200

@app.route('/ping')
def ping():
    """Endpoint de ping"""
    return "pong", 200

@app.route('/status')
def status():
    """Estado de la aplicación"""
    return jsonify({
        'status': 'running',
        'timestamp': time.time(),
        'port': os.environ.get('PORT', '5000')
    }), 200

@app.route('/detect', methods=['POST'])
def detect():
    """Endpoint de detección (simplificado)"""
    try:
        return jsonify({
            'message': 'Endpoint de detección funcionando',
            'status': 'ok',
            'timestamp': time.time()
        }), 200
    except Exception as e:
        return jsonify({
            'error': str(e),
            'timestamp': time.time()
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Iniciando aplicación en puerto {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
