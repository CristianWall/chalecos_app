#!/usr/bin/env python3
"""
Script para optimizar el modelo YOLO para despliegue
Reduce el tamaño del modelo y mejora el rendimiento
"""

import torch
from ultralytics import YOLO
import os

def optimize_model():
    """Optimizar el modelo para despliegue"""
    model_path = "modelo_entrenado/chaleco_detection/weights/best.pt"
    
    if not os.path.exists(model_path):
        print(f"Error: No se encontró el modelo en {model_path}")
        return False
    
    try:
        print("Cargando modelo original...")
        model = YOLO(model_path)
        
        # Exportar a diferentes formatos optimizados
        print("Exportando modelo a TorchScript...")
        model.export(format='torchscript', optimize=True)
        
        print("Exportando modelo a ONNX...")
        model.export(format='onnx', optimize=True)
        
        print("Exportando modelo a TensorRT (si está disponible)...")
        try:
            model.export(format='engine', half=True, workspace=4, verbose=False)
        except Exception as e:
            print(f"TensorRT no disponible: {e}")
        
        # Crear versión optimizada del modelo original
        print("Creando versión optimizada...")
        optimized_path = "modelo_entrenado/chaleco_detection/weights/best_optimized.pt"
        
        # Cargar y guardar con optimizaciones
        model_optimized = YOLO(model_path)
        
        # Compilar modelo para mejor rendimiento
        if hasattr(torch, 'compile'):
            try:
                model_optimized.model = torch.compile(model_optimized.model)
                print("Modelo compilado con torch.compile")
            except Exception as e:
                print(f"Error compilando modelo: {e}")
        
        # Guardar modelo optimizado
        torch.save(model_optimized.model.state_dict(), optimized_path)
        print(f"Modelo optimizado guardado en: {optimized_path}")
        
        # Mostrar información de tamaños
        original_size = os.path.getsize(model_path) / (1024 * 1024)  # MB
        optimized_size = os.path.getsize(optimized_path) / (1024 * 1024)  # MB
        
        print(f"\nTamaños de archivos:")
        print(f"Original: {original_size:.2f} MB")
        print(f"Optimizado: {optimized_size:.2f} MB")
        print(f"Reducción: {((original_size - optimized_size) / original_size * 100):.1f}%")
        
        return True
        
    except Exception as e:
        print(f"Error optimizando modelo: {e}")
        return False

if __name__ == "__main__":
    print("=== OPTIMIZACIÓN DE MODELO PARA DESPLIEGUE ===")
    if optimize_model():
        print("✅ Optimización completada exitosamente")
    else:
        print("❌ Error en la optimización")
