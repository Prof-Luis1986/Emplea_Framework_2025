import flet as ft
import requests
import json
import pyttsx3
import platform
import os

# Detecta el sistema operativo
SO = platform.system()

if SO == "Darwin":  # Mac
    PERSONAJE = "Albert Einstein"
    EMOJI_PERSONAJE = "🧑‍🔬"
    VOZ = "Juan"  # O la voz masculina que prefieras en Mac
elif SO == "Windows":
    PERSONAJE = "Marie Curie"
    EMOJI_PERSONAJE = "👩‍🔬"
    VOZ = "Sabina"  # O "Zira", según prefieras
else:
    PERSONAJE = "Personaje"
    EMOJI_PERSONAJE = "🧑‍🔬"
    VOZ = None  # O una voz por defecto

EMOJI_USUARIO = "🧑‍💻"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "mistral:7b"

def hablar(texto, voz=VOZ):
    if SO == "Darwin":
        # Mac: usa 'say'
        texto_limpio = texto.replace("*", "").replace("_", "").replace("#", "")
        os.system(f'say -v "{voz}" "{texto_limpio}"')
    elif SO == "Windows":
        # Windows: usa pyttsx3
        try:
            engine = pyttsx3.init()
            for v in engine.getProperty('voices'):
                if voz.lower() in v.name.lower():
                    engine.setProperty('voice', v.id)
                    break
            engine.setProperty('rate', 160)
            engine.setProperty('volume', 0.9)
            texto_limpio = texto.replace("*", "").replace("_", "").replace("#", "")
            engine.say(texto_limpio)
            engine.runAndWait()
        except Exception as e:
            print(f"Error en TTS: {e}")

def main(page: ft.Page):
    page.title = f"Chat con {PERSONAJE}"
    page.bgcolor = ft.Colors.GREY_100

    mensajes = ft.ListView(
        expand=True,
        spacing=10,
        padding=20,
        auto_scroll=True,
    )

    def burbuja(texto, es_usuario):
        return ft.Row(
            [
                ft.Text(EMOJI_USUARIO if es_usuario else EMOJI_PERSONAJE, size=24),
                ft.Container(
                    content=ft.Text(
                        texto,
                        color=ft.Colors.WHITE if es_usuario else ft.Colors.BLACK,
                        size=15,
                        selectable=True,
                    ),
                    bgcolor=ft.Colors.BLUE_400 if es_usuario else ft.Colors.GREY_300,
                    padding=12,
                    border_radius=30,
                    shadow=ft.BoxShadow(blur_radius=8, color=ft.Colors.GREY_400, offset=ft.Offset(2, 2)),
                    margin=ft.margin.only(left=10) if es_usuario else ft.margin.only(right=10),
                    alignment=ft.alignment.center_right if es_usuario else ft.alignment.center_left,
                    width=350,
                )
            ] if es_usuario else [
                ft.Container(
                    content=ft.Text(
                        texto,
                        color=ft.Colors.BLACK,
                        size=15,
                        selectable=True,
                    ),
                    bgcolor=ft.Colors.GREY_300,
                    padding=12,
                    border_radius=30,
                    shadow=ft.BoxShadow(blur_radius=8, color=ft.Colors.GREY_400, offset=ft.Offset(2, 2)),
                    margin=ft.margin.only(right=10),
                    alignment=ft.alignment.center_left,
                    width=350,
                ),
                ft.Text(EMOJI_PERSONAJE, size=24),
            ],
            alignment=ft.MainAxisAlignment.END if es_usuario else ft.MainAxisAlignment.START,
        )

    prompt = ft.TextField(
        label=f"Escribe tu mensaje...",
        expand=True,
        border_radius=20,
        filled=True,
        bgcolor=ft.Colors.WHITE
    )

    voz_activada = ft.Checkbox(label="🔊 Leer respuestas en voz alta", value=True)

    def enviar_click(e):
        user_input = prompt.value.strip()
        if not user_input:
            return
        mensajes.controls.append(burbuja(user_input, es_usuario=True))
        page.update()
        prompt.value = ""
        page.update()

        prompt_personaje = (
            f"Responde como si fueras {PERSONAJE}. "
            "Habla con su estilo, conocimientos y personalidad. "
            "Responde en español de manera clara y concisa. "
            f"Pregunta del usuario: {user_input}"
        )

        try:
            response = requests.post(
                OLLAMA_URL,
                json={"model": MODEL, "prompt": prompt_personaje, "stream": True},
                stream=True
            )
            respuesta = ""
            for line in response.iter_lines():
                if line:
                    data = json.loads(line)
                    if "response" in data:
                        respuesta += data["response"]
                    elif "error" in data:
                        respuesta = f"Error de Ollama: {data['error']}"
                        break
            if not respuesta:
                respuesta = "No se recibió respuesta del modelo."
        except Exception as ex:
            respuesta = f"Error de conexión o inesperado: {ex}"

        mensajes.controls.append(burbuja(respuesta, es_usuario=False))
        page.update()

        # Leer la respuesta en voz alta si está activado
        if voz_activada.value and VOZ:
            try:
                hablar(respuesta, voz=VOZ)
            except Exception as ex:
                print(f"Error en text-to-speech: {ex}")

    prompt.on_submit = enviar_click

    def probar_voz(e):
        if VOZ:
            hablar(f"Hola, soy {PERSONAJE}. Esta es mi voz.", voz=VOZ)

    header = ft.Container(
        content=ft.Row([
            ft.Text(EMOJI_PERSONAJE, size=32),
            ft.Text(PERSONAJE, size=22, weight="bold", color=ft.Colors.BLUE_900),
        ], alignment=ft.MainAxisAlignment.START, spacing=15),
        padding=ft.padding.symmetric(vertical=16, horizontal=10),
        bgcolor=ft.Colors.WHITE,
        border_radius=ft.border_radius.only(top_left=20, top_right=20),
        shadow=ft.BoxShadow(blur_radius=12, color=ft.Colors.GREY_300, offset=ft.Offset(0, 2))
    )

    page.add(
        ft.Container(
            content=ft.Column([
                header,
                mensajes,
                ft.Row([
                    voz_activada,
                    ft.ElevatedButton(
                        "🎤 Probar voz", 
                        on_click=probar_voz, 
                        bgcolor=ft.Colors.GREEN_400, 
                        color=ft.Colors.WHITE
                    )
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                ft.Row([
                    prompt, 
                    ft.ElevatedButton(
                        "Enviar", 
                        on_click=enviar_click, 
                        bgcolor=ft.Colors.BLUE_400, 
                        color=ft.Colors.WHITE
                    )
                ], vertical_alignment=ft.CrossAxisAlignment.END),
            ], expand=True, spacing=10),
            expand=True,
            padding=0,
            border_radius=0,
            bgcolor=ft.Colors.WHITE,
        )
    )

ft.app(target=main)
