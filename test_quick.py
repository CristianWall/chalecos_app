#!/usr/bin/env python3
"""
Prueba rápida del sistema de detección de chalecos
"""

from app import app, model

print("🦺 PRUEBA RÁPIDA - DETECCIÓN DE CHALECOS")
print("=" * 40)

# Verificar modelo
if model is not None:
    print("✅ Modelo YOLO cargado correctamente")
else:
    print("❌ Error: No se pudo cargar el modelo")

# Verificar aplicación
try:
    print("✅ Aplicación Flask creada correctamente")
    print("\n🚀 Para ejecutar:")
    print("   python app.py")
    print("\n🌐 Luego abre: http://localhost:5000")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n✅ Prueba completada")
