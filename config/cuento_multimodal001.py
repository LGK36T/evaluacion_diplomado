# apps/gui_cuento_multimodal.py
from __future__ import annotations
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
import threading, datetime, base64, sys, os  # <- incluye os
from typing import Optional

# --- Ruta proyecto para imports ---
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# --- Cliente OpenAI (usa tu config/settings.py) ---
from config.settings import client


# ========= Utilidades =========
def ts_now() -> str:
    """Timestamp único por ejecución (AAAAmmdd_HHMMSS)."""
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

def ensure_dir(p: Path) -> Path:
    p.mkdir(parents=True, exist_ok=True)
    return p

def safe_write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


# ========= Núcleo de generación =========
def generate_story(tema: str, grado: int, model: str = "gpt-4.1-mini", temperature: float = 0.7) -> str:
    system = (
        "Eres un docente de Lenguaje para educación básica en Chile. "
        "Escribe cuentos breves, positivos y adecuados a la edad. Evita contenido sensible. "
        "Cuida ortografía y puntuación."
    )
    reglas = {
        1: "120–160 palabras; oraciones cortas; vocabulario muy simple; 1 idea central.",
        2: "150–200 palabras; inicio–nudo–desenlace claros; vocabulario simple.",
        3: "180–240 palabras; personajes con rasgos simples; moraleja explícita.",
        4: "220–280 palabras; descripciones un poco más ricas; cierre reflexivo."
    }
    guia = reglas.get(int(grado), reglas[3])
    user = (
        f"Tema del cuento: {tema}\n"
        f"Grado: {grado}° básico\n\n"
        "Instrucciones:\n"
        f"- Extensión y estilo: {guia}\n"
        "- Tono cálido y motivador.\n"
        "- Incluye nombres y acciones concretas que ayuden a visualizar la escena.\n"
        "- Lenguaje inclusivo y respetuoso.\n"
        "- Devuelve SOLO el cuento (sin títulos, listas ni comentarios)."
    )
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": system},
                  {"role": "user", "content": user}],
        max_tokens=650,
        temperature=temperature,
    )
    return (resp.choices[0].message.content or "").strip()

def generate_image(descripcion: str, outdir: Path, stamp: str, size: str = "1024x1024", model: str = "gpt-image-1") -> Path:
    ensure_dir(outdir)
    prompt = (
        "Ilustración infantil para cuento escolar, estilo limpio, colores suaves, "
        "personajes amables, sin texto sobre la imagen. Escena: " + descripcion
    )
    img = client.images.generate(
        model=model,
        prompt=prompt,
        size=size,
        quality="high",           # ✅ corregido (valores válidos: low/medium/high/auto)
        n=1
    )
    b64 = img.data[0].b64_json
    png_bytes = base64.b64decode(b64)
    out = outdir / f"ilustracion_{stamp}.png"
    out.write_bytes(png_bytes)
    return out

def generate_audio(texto: str, outdir: Path, stamp: str, tts_model: str = "gpt-4o-mini-tts", voice: str = "alloy") -> Path:
    ensure_dir(outdir)
    out = outdir / f"cuento_{stamp}.mp3"
    with client.audio.speech.with_streaming_response.create(
        model=tts_model,
        voice=voice,
        input=texto
    ) as resp:
        resp.stream_to_file(out)
    return out


# ========= GUI =========
class App(ttk.Frame):
    def __init__(self, master: tk.Tk):
        super().__init__(master, padding=12)
        self.master.title("Generador Multimodal de Cuentos (OpenAI)")
        self.master.geometry("780x560")
        self.grid(sticky="nsew")

        # Vars
        self.var_tema = tk.StringVar()
        self.var_grado = tk.StringVar(value="3")
        self.var_modelo = tk.StringVar(value="gpt-4.1-mini")
        self.var_tts = tk.StringVar(value="gpt-4o-mini-tts")
        self.var_voz = tk.StringVar(value="alloy")
        self.var_size = tk.StringVar(value="1024x1024")
        self.var_outdir = tk.StringVar(value=str((ROOT / "outputs").resolve()))
        self.var_temp = tk.DoubleVar(value=0.7)
        self.var_auto_desc = tk.BooleanVar(value=True)  # autogenerar descripción desde cuento

        # Layout responsive
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        for r in (4, 6):
            self.rowconfigure(r, weight=1)
        self.columnconfigure(1, weight=1)

        # Campos
        ttk.Label(self, text="Tema del cuento:").grid(row=0, column=0, sticky="w", pady=2)
        ttk.Entry(self, textvariable=self.var_tema).grid(row=0, column=1, columnspan=3, sticky="ew", padx=6, pady=2)

        ttk.Label(self, text="Curso (1–8):").grid(row=1, column=0, sticky="w", pady=2)
        ttk.Entry(self, width=6, textvariable=self.var_grado).grid(row=1, column=1, sticky="w", padx=6, pady=2)

        ttk.Label(self, text="Modelo texto:").grid(row=2, column=0, sticky="w", pady=2)
        ttk.Combobox(self, textvariable=self.var_modelo, values=["gpt-4.1-mini","gpt-4o","gpt-5-mini","gpt-3.5-turbo"], width=18).grid(row=2, column=1, sticky="w", padx=6, pady=2)

        ttk.Label(self, text="TTS:").grid(row=2, column=2, sticky="e", padx=(20,4))
        ttk.Combobox(self, textvariable=self.var_tts, values=["gpt-4o-mini-tts","tts-1","tts-1-hd"], width=16).grid(row=2, column=3, sticky="w")

        ttk.Label(self, text="Voz:").grid(row=1, column=2, sticky="e", padx=(20,4))
        ttk.Entry(self, textvariable=self.var_voz, width=16).grid(row=1, column=3, sticky="w")

        ttk.Label(self, text="Tamaño imagen:").grid(row=0, column=4, sticky="e", padx=(20,4))
        ttk.Combobox(self, textvariable=self.var_size, values=["512x512","1024x1024"], width=12).grid(row=0, column=5, sticky="w")

        ttk.Label(self, text="Temperature:").grid(row=3, column=0, sticky="w", pady=2)
        ttk.Scale(self, from_=0.0, to=1.0, orient="horizontal", variable=self.var_temp).grid(row=3, column=1, columnspan=2, sticky="ew", padx=6)

        ttk.Checkbutton(self, text="Autogenerar descripción de imagen desde el cuento", variable=self.var_auto_desc).grid(row=3, column=3, columnspan=3, sticky="w")

        ttk.Label(self, text="Carpeta salida:").grid(row=4, column=0, sticky="w", pady=(8,2))
        out_entry = ttk.Entry(self, textvariable=self.var_outdir)
        out_entry.grid(row=4, column=1, columnspan=4, sticky="ew", padx=6)
        ttk.Button(self, text="Elegir…", command=self.choose_dir).grid(row=4, column=5, sticky="e", padx=4)

        # Botones
        btns = ttk.Frame(self)
        btns.grid(row=5, column=0, columnspan=6, sticky="ew", pady=10)
        for i in range(6):
            btns.columnconfigure(i, weight=1)
        ttk.Button(btns, text="Generar TODO", command=self.on_todo).grid(row=0, column=0, padx=4, sticky="ew")
        ttk.Button(btns, text="Solo Cuento", command=self.on_cuento).grid(row=0, column=1, padx=4, sticky="ew")
        ttk.Button(btns, text="Solo Imagen", command=self.on_imagen).grid(row=0, column=2, padx=4, sticky="ew")
        ttk.Button(btns, text="Solo Audio", command=self.on_audio).grid(row=0, column=3, padx=4, sticky="ew")
        ttk.Button(btns, text="Abrir carpeta", command=self.open_outdir).grid(row=0, column=4, padx=4, sticky="ew")
        ttk.Button(btns, text="Salir", command=self.master.destroy).grid(row=0, column=5, padx=4, sticky="ew")

        # Log
        ttk.Label(self, text="Registro:").grid(row=6, column=0, sticky="w", pady=(6,2))
        self.txt = tk.Text(self, height=12, wrap="word")
        self.txt.grid(row=7, column=0, columnspan=6, sticky="nsew")
        self.scroll = ttk.Scrollbar(self, command=self.txt.yview)
        self.scroll.grid(row=7, column=6, sticky="ns")
        self.txt.configure(yscrollcommand=self.scroll.set)

        # Estado
        self.busy = False

    # ----- helpers GUI -----
    def log(self, msg: str):
        self.txt.insert("end", msg + "\n")
        self.txt.see("end")
        self.txt.update_idletasks()

    def choose_dir(self):
        sel = filedialog.askdirectory(initialdir=self.var_outdir.get() or str(ROOT))
        if sel:
            self.var_outdir.set(sel)

    def open_outdir(self):
        try:
            p = Path(self.var_outdir.get()).resolve()
            ensure_dir(p)
            if sys.platform.startswith("win"):
                os.startfile(str(p))
            elif sys.platform == "darwin":
                import subprocess; subprocess.Popen(["open", str(p)])
            else:
                import subprocess; subprocess.Popen(["xdg-open", str(p)])
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir la carpeta:\n{e}")

    def _validate_inputs(self) -> tuple[str,int,Path,str,str,str,float,str]:
        tema = self.var_tema.get().strip()
        if not tema:
            raise ValueError("Tema requerido.")
        try:
            grado = int(self.var_grado.get().strip())
        except:
            raise ValueError("Grado debe ser entero (1–4).")
        if grado not in (1,2,3,4):
            raise ValueError("Grado debe ser 1, 2, 3 o 4.")
        outdir = Path(self.var_outdir.get()).expanduser()
        model = self.var_modelo.get().strip()
        tts_model = self.var_tts.get().strip()
        voice = self.var_voz.get().strip()
        size = self.var_size.get().strip()
        temp = float(self.var_temp.get())
        stamp = ts_now()
        return tema, grado, outdir, model, tts_model, voice, temp, stamp

    # ----- acciones threaded -----
    def on_todo(self):
        self._run_threaded(self._do_todo)

    def on_cuento(self):
        self._run_threaded(self._do_cuento)

    def on_imagen(self):
        self._run_threaded(self._do_imagen)

    def on_audio(self):
        self._run_threaded(self._do_audio)

    def _run_threaded(self, target):
        if self.busy:
            messagebox.showinfo("En progreso", "Espera a que termine la tarea actual.")
            return
        self.busy = True
        t = threading.Thread(target=self._guard(target), daemon=True)
        t.start()

    def _guard(self, target):
        def runner():
            try:
                target()
            except Exception as e:
                self.log(f"❌ {e}")
                messagebox.showerror("Error", str(e))
            finally:
                self.busy = False
        return runner

    # ----- tareas -----
    def _do_todo(self):
        tema, grado, outdir, model, tts_model, voice, temp, stamp = self._validate_inputs()
        ensure_dir(outdir)

        self.log("📝 Generando cuento…")
        cuento = generate_story(tema, grado, model=model, temperature=temp)
        cuento_path = outdir / f"cuento_{stamp}.txt"
        safe_write_text(cuento_path, cuento)
        self.log(f"✅ Cuento: {cuento_path}")

        self.log("🎨 Generando ilustración…")
        if self.var_auto_desc.get():
            breve = " ".join([s.strip() for s in cuento.split(".") if s.strip()][:3])[:300]
            desc = breve or f"Escena principal del cuento sobre {tema}"
        else:
            desc = f"Escena principal del cuento sobre {tema}"
        img_path = generate_image(desc, outdir=outdir, stamp=stamp, size=self.var_size.get())
        self.log(f"✅ Imagen: {img_path}")

        self.log("🔊 Generando audio…")
        mp3_path = generate_audio(cuento, outdir=outdir, stamp=stamp, tts_model=tts_model, voice=voice)
        self.log(f"✅ Audio: {mp3_path}")

        messagebox.showinfo("Listo", "Cuento, imagen y audio generados.")

    def _do_cuento(self):
        tema, grado, outdir, model, tts_model, voice, temp, stamp = self._validate_inputs()
        ensure_dir(outdir)

        self.log("📝 Generando cuento…")
        cuento = generate_story(tema, grado, model=model, temperature=temp)
        cuento_path = outdir / f"cuento_{stamp}.txt"
        safe_write_text(cuento_path, cuento)
        self.log(f"✅ Cuento: {cuento_path}")
        messagebox.showinfo("Listo", f"Cuento guardado en:\n{cuento_path}")

    def _do_imagen(self):
        tema, grado, outdir, model, tts_model, voice, temp, stamp = self._validate_inputs()
        ensure_dir(outdir)

        self.log("🎨 Generando ilustración…")
        desc = f"Escena principal del cuento sobre {tema}"
        img_path = generate_image(desc, outdir=outdir, stamp=stamp, size=self.var_size.get())
        self.log(f"✅ Imagen: {img_path}")
        messagebox.showinfo("Listo", f"Imagen guardada en:\n{img_path}")

    def _do_audio(self):
        tema, grado, outdir, model, tts_model, voice, temp, stamp = self._validate_inputs()
        ensure_dir(outdir)

        self.log("📝 Generando cuento para narrar…")
        cuento = generate_story(tema, grado, model=model, temperature=temp)
        cuento_path = outdir / f"cuento_{stamp}.txt"
        safe_write_text(cuento_path, cuento)
        self.log(f"✅ Cuento: {cuento_path}")

        self.log("🔊 Generando audio…")
        mp3_path = generate_audio(cuento, outdir=outdir, stamp=stamp, tts_model=tts_model, voice=voice)
        self.log(f"✅ Audio: {mp3_path}")
        messagebox.showinfo("Listo", f"Audio guardado en:\n{mp3_path}")


def main():
    root = tk.Tk()
    # Tema ttk básico
    try:
        style = ttk.Style()
        style.theme_use("clam")
    except Exception:
        pass
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
