# config/main.py
from __future__ import annotations
from config.settings import client

from colorama import Fore, Style, init

# === Preferencias del chat ===
MODEL = "gpt-4o"   # "gpt-4o", "gpt-4.1-mini", etc.
MAX_TOKENS = 200
TEMPERATURE = 0.7
SHOW_MODELS_ON_START = True

init(autoreset=True)

def run_chat():
    print(Fore.CYAN + "💬 Chat iniciado. Escribe 'salir' para terminar. Comandos: /reset\n")

    history = [{"role": "system", "content": "Eres un asistente útil, claro y amigable."}]

    if SHOW_MODELS_ON_START:
        try:
            models = client.models.list()
            print(Fore.MAGENTA + "📦 Modelos disponibles (primeros 20):")
            for m in models.data[:20]:
                print(Fore.MAGENTA + f"   🔹 {m.id}")
            print()
        except Exception as e:
            print(Fore.RED + f"⚠️ No pude listar modelos: {e}\n")

    while True:
        user_input = input(Fore.YELLOW + "👤 Tú: ").strip()

        if user_input.lower() in {"salir", "exit", "quit"}:
            print(Fore.MAGENTA + "👋 ¡Hasta luego!")
            break

        if user_input.lower() == "/reset":
            history = history[:1]
            print(Fore.BLUE + "♻️  Historial reiniciado.\n")
            continue

        history.append({"role": "user", "content": user_input})

        try:
            resp = client.chat.completions.create(
                model=MODEL,
                messages=history,
                max_tokens=MAX_TOKENS,
                temperature=TEMPERATURE,
            )
            msg = (resp.choices[0].message.content or "").strip()
            print(Fore.GREEN + "🤖 IA:" + Fore.WHITE + f" {msg}\n")
            history.append({"role": "assistant", "content": msg})

        except Exception as e:
            print(Fore.RED + f"❌ Error: {e}\n")

if __name__ == "__main__":
    run_chat()
