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
.\venv\Scripts\activate   # en Windows
source venv/bin/activate  # en Linux/Mac
```

### 2. Instalar librerías necesarias  
```bash
pip install openai python-dotenv colorama pillow tk
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
py -m config.main
```

---

## ▶️ Ejecución  

### 1. Desde consola (modo script)  
Generar un cuento completo (texto + imagen + audio):  
```bash
py -m config.cuento_multimodal --tema "La amistad" --grado 3
```

Los archivos se guardarán en `outputs/` con **timestamp** (ej: `cuento_20250822_213500.txt`).  

---

### 2. Desde GUI (modo gráfico con Tkinter)  
Ejecuta:  
```bash
py -m apps.gui_cuento_multimodal
```

La ventana permite elegir:  
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
│   ├── settings.py          # Configuración API y cliente OpenAI
│   ├── main.py              # Chat simple de prueba
│   ├── cuento_multimodal.py # Script consola (texto+imagen+audio)
│── apps/
│   ├── gui_cuento_multimodal.py # Interfaz gráfica Tkinter
│── outputs/                 # Carpeta de resultados generados
│── .env                     # Clave de API (NO subir a GitHub)
│── requirements.txt         # Dependencias
```

---

## 📦 requirements.txt  

Si quieres instalar en otro PC, crea este archivo:  

```aiohappyeyeballs==2.6.1
aiohttp==3.12.15
aiosignal==1.4.0
annotated-types==0.7.0
anyio==4.10.0
attrs==25.3.0
certifi==2025.1.31
charset-normalizer==3.4.1
colorama==0.4.6
distro==1.9.0
frozenlist==1.7.0
h11==0.16.0
httpcore==1.0.9
httpx==0.28.1
idna==3.10
jiter==0.10.0
multidict==6.6.3
openai==0.28.0
pdfkit==1.0.0
propcache==0.3.2
pydantic==2.11.7
pydantic_core==2.33.2
PyQt5==5.15.11
PyQt5-Qt5==5.15.2
PyQt5_sip==12.17.0
python-dotenv==1.1.1
python-vlc==3.0.21203
requests==2.32.3
sniffio==1.3.1
tqdm==4.67.1
typing-inspection==0.4.1
typing_extensions==4.14.1
urllib3==2.3.0
yarl==1.20.1
```

Y ejecuta:  
```bash
pip install -r requirements.txt
```

---

## ✨ Ejemplo de uso  

```bash
py -m config.cuento_multimodal 
```

📂 Salida:  
- `cuento_20250822_213500.txt` → Texto del cuento  
- `ilustracion_20250822_213500.png` → Imagen ilustrativa  
- `cuento_20250822_213500.mp3` → Narración en audio  
