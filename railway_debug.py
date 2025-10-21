#!/usr/bin/env python3
"""
Script de diagnóstico específico para Railway
"""

import os
import sys

def check_port_config():
    """Verificar configuración del puerto"""
    print("🔍 Verificando configuración del puerto...")
    
    port = os.environ.get('PORT', '5000')
    print(f"✅ Puerto configurado: {port}")
    
    return True

def check_flask_app():
    """Verificar que la aplicación Flask se puede crear"""
    print("\n🚀 Verificando aplicación Flask...")
    
    try:
        from flask import Flask
        app = Flask(__name__)
        
        @app.route('/health')
        def health():
            return "OK", 200
        
        @app.route('/ping')
        def ping():
            return "pong", 200
        
        print("✅ Aplicación Flask creada correctamente")
        print("✅ Endpoints /health y /ping configurados")
        
        return True
    except Exception as e:
        print(f"❌ Error creando aplicación Flask: {e}")
        return False

def check_dependencies():
    """Verificar dependencias críticas"""
    print("\n📦 Verificando dependencias...")
    
    dependencies = [
        'flask',
        'gunicorn',
        'ultralytics',
        'opencv-python-headless',
        'numpy',
        'pillow'
    ]
    
    for dep in dependencies:
        try:
            __import__(dep.replace('-', '_'))
            print(f"✅ {dep}")
        except ImportError:
            print(f"❌ {dep} - No encontrado")
            return False
    
    return True

def check_model_file():
    """Verificar archivo del modelo"""
    print("\n🤖 Verificando archivo del modelo...")
    
    model_path = "modelo_entrenado/chaleco_detection/weights/best.pt"
    
    if os.path.exists(model_path):
        size = os.path.getsize(model_path) / (1024 * 1024)  # MB
        print(f"✅ Modelo encontrado: {model_path} ({size:.2f} MB)")
        return True
    else:
        print(f"❌ Modelo no encontrado: {model_path}")
        return False

def check_environment():
    """Verificar variables de entorno"""
    print("\n🌍 Verificando variables de entorno...")
    
    env_vars = ['PORT', 'FLASK_ENV']
    
    for var in env_vars:
        value = os.environ.get(var, 'No configurado')
        print(f"✅ {var}: {value}")
    
    return True

def main():
    """Función principal"""
    print("🔧 DIAGNÓSTICO RAILWAY")
    print("=" * 50)
    
    tests = [
        check_port_config,
        check_dependencies,
        check_flask_app,
        check_model_file,
        check_environment
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
        print("\n🚀 Próximos pasos:")
        print("1. git add .")
        print("2. git commit -m 'Fix: Configuración Railway'")
        print("3. git push origin main")
        return True
    else:
        print("❌ Algunas pruebas fallaron")
        print("🔧 Revisa los errores antes de desplegar")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
