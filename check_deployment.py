#!/usr/bin/env python3
"""
Script para verificar que todo esté listo para el despliegue en Railway
"""

import os
import sys
from pathlib import Path

def check_file_exists(filepath, description):
    """Verificar que un archivo existe"""
    if Path(filepath).exists():
        size = Path(filepath).stat().st_size / (1024 * 1024)  # MB
        print(f"✅ {description}: {filepath} ({size:.2f} MB)")
        return True
    else:
        print(f"❌ {description}: {filepath} - NO ENCONTRADO")
        return False

def check_deployment():
    """Verificar que todo esté listo para el despliegue"""
    print("🔍 VERIFICANDO PREPARACIÓN PARA DESPLIEGUE EN RAILWAY")
    print("=" * 60)
    
    checks_passed = 0
    total_checks = 0
    
    # Archivos principales
    files_to_check = [
        ("app.py", "Aplicación Flask principal"),
        ("requirements.txt", "Dependencias Python"),
        ("Dockerfile", "Configuración Docker"),
        ("railway.json", "Configuración Railway"),
        ("README.md", "Documentación"),
        ("templates/index.html", "Interfaz web"),
        ("modelo_entrenado/chaleco_detection/weights/best.pt", "Modelo YOLO")
    ]
    
    for filepath, description in files_to_check:
        total_checks += 1
        if check_file_exists(filepath, description):
            checks_passed += 1
    
    print("\n" + "=" * 60)
    print(f"📊 RESULTADO: {checks_passed}/{total_checks} verificaciones pasaron")
    
    # Verificar tamaño total del modelo
    model_path = "modelo_entrenado/chaleco_detection/weights/best.pt"
    if Path(model_path).exists():
        model_size = Path(model_path).stat().st_size / (1024 * 1024)
        print(f"📦 Tamaño del modelo: {model_size:.2f} MB")
        
        if model_size > 100:  # 100MB
            print("⚠️  ADVERTENCIA: El modelo es bastante grande")
            print("   Considera optimizarlo ejecutando: python optimize_model.py")
    
    # Verificar límite de 4GB
    total_size = 0
    for root, dirs, files in os.walk("."):
        for file in files:
            filepath = Path(root) / file
            if filepath.exists():
                total_size += filepath.stat().st_size
    
    total_size_mb = total_size / (1024 * 1024)
    print(f"📊 Tamaño total del proyecto: {total_size_mb:.2f} MB")
    
    if total_size_mb > 4000:  # 4GB
        print("❌ ERROR: El proyecto excede el límite de 4GB de Railway")
        return False
    elif total_size_mb > 2000:  # 2GB
        print("⚠️  ADVERTENCIA: El proyecto es grande, pero dentro del límite")
    else:
        print("✅ Tamaño del proyecto dentro del límite recomendado")
    
    print("\n" + "=" * 60)
    
    if checks_passed == total_checks:
        print("🎉 ¡TODO LISTO PARA DESPLEGAR!")
        print("\n📋 Próximos pasos:")
        print("1. git add .")
        print("2. git commit -m 'Deploy app'")
        print("3. git push origin main")
        print("4. Conectar con Railway desde GitHub")
        print("\n📖 Consulta README.md para instrucciones detalladas")
        return True
    else:
        print("❌ Faltan archivos necesarios para el despliegue")
        print("Revisa los errores anteriores antes de continuar")
        return False

if __name__ == "__main__":
    success = check_deployment()
    sys.exit(0 if success else 1)
