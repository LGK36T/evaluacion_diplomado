# 📖 Generador Multimodal de Cuentos con OpenAI  

Este proyecto permite generar cuentos personalizados para distintos niveles escolares usando **OpenAI**.  
Incluye:  
- ✍️ **Texto** (cuento educativo según tema y curso)  
- 🎨 **Imagen ilustrativa** (IA generativa estilo infantil)  
- 🔊 **Narración en audio** (TTS con voces naturales)  
- 🖥️ **Interfaz gráfica (Tkinter)** para usarlo de forma sencilla  

---

## 🚀 Requisitos  

### 1. Python  
- Versión recomendada: **3.10+**  
- Crear entorno virtual:  
```bash
py -m venv venv
.\venv\Scripts\activate.bat   # En Windows CMD
.\venv\Scripts\activate.ps    # En windows powershell
source venv/bin/activate      # En Linux/Mac
```

### 2. Instalar librerías necesarias  
## 📦 requirements.txt  

Si quieres instalar en otro PC puedes realizar la instalacion de dependencias con el archivo requirements.txt, solo debes ejecutar el siguiente codigo:  

```bash
pip install -r requirements.txt
```
---

## ⚙️ Configuración  

1. Crea un archivo **.env** en la raíz del proyecto con tu API Key:  
```env
OPENAI_API_KEY=sk-xxxxxx_tu_api_key_aqui
```

👉 También puedes generarlo directo desde PowerShell:  
```powershell
echo "OPENAI_API_KEY=sk-xxxxxx_tu_api_key_aqui" > .env
```

2. Verifica que funciona probando en consola:  
```bash
python -m config.cuento_multimodal
```

---

## ▶️ Ejecución  

### 1. Desde GUI (modo gráfico con Tkinter)  
Ejecuta:  
```bash
python -m config.cuento_multimodal
```

El programa abre una ventana que permite elegir:  
- Tema del cuento  
- Curso (1° a 4° básico)  
- Modelo de texto y voz  
- Carpeta de salida  
- Y botones: Generar cuento, imagen, audio o todo junto  

---

## 📂 Estructura del proyecto  

```
Proyecto_01/
│── config/
│   ├── __init__.py 
│   ├── settings.py          # Configuración API y cliente OpenAI
│   ├── cuento_multimodal.py # Gui con tkinter (texto+imagen+audio)
│── outputs/                 # Carpeta de resultados generados
│── .env                     # Clave de API (NO subir a GitHub)
│── requirements.txt         # Dependencias
```
---

## ✨ Ejemplo de uso  

```bash
python -m config.cuento_multimodal 
```

📂 Salida:  
- `cuento_20250822_213500.txt` → Texto del cuento  
- `ilustracion_20250822_213500.png` → Imagen ilustrativa  
- `cuento_20250822_213500.mp3` → Narración en audio  
