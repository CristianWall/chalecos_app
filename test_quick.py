#!/usr/bin/env python3
"""
Script de prueba rápida para verificar la aplicación
"""

import os
import sys

def test_imports():
    """Probar que todas las importaciones funcionan"""
    print("🔍 Probando importaciones...")
    
    try:
        import flask
        print("✅ Flask importado")
    except Exception as e:
        print(f"❌ Error importando Flask: {e}")
        return False
    
    try:
        import cv2
        print("✅ OpenCV importado")
    except Exception as e:
        print(f"❌ Error importando OpenCV: {e}")
        return False
    
    try:
        import numpy as np
        print("✅ NumPy importado")
    except Exception as e:
        print(f"❌ Error importando NumPy: {e}")
        return False
    
    try:
        from ultralytics import YOLO
        print("✅ Ultralytics importado")
    except Exception as e:
        print(f"❌ Error importando Ultralytics: {e}")
        return False
    
    return True

def test_model_file():
    """Probar que el archivo del modelo existe"""
    print("\n🤖 Probando archivo del modelo...")
    
    model_path = "modelo_entrenado/chaleco_detection/weights/best.pt"
    
    if os.path.exists(model_path):
        size = os.path.getsize(model_path) / (1024 * 1024)  # MB
        print(f"✅ Modelo encontrado: {model_path} ({size:.2f} MB)")
        return True
    else:
        print(f"❌ Modelo no encontrado: {model_path}")
        return False

def test_app_import():
    """Probar que la aplicación se puede importar"""
    print("\n🚀 Probando importación de la aplicación...")
    
    try:
        # Cambiar al directorio de la aplicación
        import app
        print("✅ Aplicación importada correctamente")
        return True
    except Exception as e:
        print(f"❌ Error importando aplicación: {e}")
        return False

def main():
    """Función principal"""
    print("🧪 PRUEBA RÁPIDA DE LA APLICACIÓN")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_model_file,
        test_app_import
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 RESULTADO: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡Todas las pruebas pasaron!")
        print("✅ La aplicación debería funcionar en Railway")
        return True
    else:
        print("❌ Algunas pruebas fallaron")
        print("🔧 Revisa los errores antes de desplegar")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
