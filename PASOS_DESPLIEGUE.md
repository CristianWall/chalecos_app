# 🚀 PASOS RÁPIDOS PARA DESPLEGAR EN HEROKU

## ⚡ Comandos para Ejecutar (Copia y Pega)

### 1. Navegar a la carpeta de despliegue
```bash
cd despliegue
```

### 2. Iniciar sesión en Heroku
```bash
heroku login
```

### 3. Inicializar Git
```bash
git init
```

### 4. Crear aplicación en Heroku (cambia el nombre)
```bash
heroku create mi-app-chalecos-2024
```

### 5. Agregar archivos a Git
```bash
git add .
```

### 6. Hacer commit
```bash
git commit -m "App detección de chalecos - Primera versión"
```

### 7. Desplegar en Heroku
```bash
git push heroku main
```

### 8. Abrir la aplicación
```bash
heroku open
```

---

## 🎯 ¡LISTO! 

Tu aplicación estará disponible en: `https://mi-app-chalecos-2024.herokuapp.com`

## 🔧 Si algo sale mal:

### Ver errores:
```bash
heroku logs --tail
```

### Reiniciar aplicación:
```bash
heroku restart
```

### Ver estado:
```bash
heroku ps
```

---

## 📱 Cómo usar la app:

1. **Abre el enlace** en tu navegador
2. **Permite acceso a la cámara**
3. **Haz clic en "Iniciar Cámara"**
4. **Posiciónate frente a la cámara**
5. **Haz clic en "Capturar y Detectar"**
6. **¡Ve los resultados!**

---

**¡Tu app de detección de chalecos estará funcionando en la web! 🌐✨**
