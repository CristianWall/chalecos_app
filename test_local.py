#!/usr/bin/env python3
"""
Script para probar la aplicación localmente antes del despliegue
"""

import requests
import time
import subprocess
import sys
import os

def test_health_endpoints():
    """Probar endpoints de salud"""
    base_url = "http://localhost:5000"
    
    print("🔍 Probando endpoints de salud...")
    
    # Probar /ping
    try:
        response = requests.get(f"{base_url}/ping", timeout=10)
        if response.status_code == 200:
            print("✅ /ping - OK")
        else:
            print(f"❌ /ping - Error {response.status_code}")
    except Exception as e:
        print(f"❌ /ping - Error: {e}")
    
    # Probar /health
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            print("✅ /health - OK")
            data = response.json()
            print(f"   Status: {data.get('status')}")
            print(f"   Model: {data.get('model_status')}")
        else:
            print(f"❌ /health - Error {response.status_code}")
    except Exception as e:
        print(f"❌ /health - Error: {e}")
    
    # Probar página principal
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        if response.status_code == 200:
            print("✅ / - OK")
        else:
            print(f"❌ / - Error {response.status_code}")
    except Exception as e:
        print(f"❌ / - Error: {e}")

def check_model_loading():
    """Verificar que el modelo se carga correctamente"""
    print("\n🤖 Verificando carga del modelo...")
    
    try:
        from ultralytics import YOLO
        model_path = "modelo_entrenado/chaleco_detection/weights/best.pt"
        
        if not os.path.exists(model_path):
            print(f"❌ Modelo no encontrado: {model_path}")
            return False
        
        print(f"✅ Modelo encontrado: {model_path}")
        
        # Intentar cargar el modelo
        model = YOLO(model_path)
        print("✅ Modelo cargado exitosamente")
        
        # Verificar clases
        if hasattr(model, 'names'):
            print(f"✅ Clases del modelo: {list(model.names.values())}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error cargando modelo: {e}")
        return False

def start_app():
    """Iniciar la aplicación para pruebas"""
    print("🚀 Iniciando aplicación para pruebas...")
    
    try:
        # Iniciar la aplicación en background
        process = subprocess.Popen([
            sys.executable, "app.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Esperar un poco para que inicie
        time.sleep(5)
        
        # Verificar que el proceso esté corriendo
        if process.poll() is None:
            print("✅ Aplicación iniciada")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Error iniciando aplicación:")
            print(f"STDOUT: {stdout.decode()}")
            print(f"STDERR: {stderr.decode()}")
            return None
            
    except Exception as e:
        print(f"❌ Error iniciando aplicación: {e}")
        return None

def main():
    """Función principal"""
    print("🧪 DIAGNÓSTICO DE LA APLICACIÓN")
    print("=" * 50)
    
    # Verificar modelo
    model_ok = check_model_loading()
    
    if not model_ok:
        print("\n❌ El modelo no se puede cargar. Revisa la configuración.")
        return False
    
    # Iniciar aplicación
    process = start_app()
    
    if process is None:
        print("\n❌ No se pudo iniciar la aplicación.")
        return False
    
    try:
        # Probar endpoints
        test_health_endpoints()
        
        print("\n🎉 Diagnóstico completado!")
        print("Si todos los tests pasan, la aplicación debería funcionar en Railway.")
        
    finally:
        # Terminar proceso
        if process:
            process.terminate()
            process.wait()
            print("\n🛑 Aplicación detenida")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
