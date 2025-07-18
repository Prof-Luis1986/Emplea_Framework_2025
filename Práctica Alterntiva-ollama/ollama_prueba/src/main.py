import flet as ft
import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "mistral:7b"
PERSONAJE = "Albert Einstein"
EMOJI_PERSONAJE = "🧑‍🔬"
EMOJI_USUARIO = "🧑‍💻"

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

    # Header con emoji y nombre
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
                ft.Row([prompt, ft.ElevatedButton("Enviar", on_click=enviar_click, bgcolor=ft.Colors.BLUE_400, color=ft.Colors.WHITE)], vertical_alignment=ft.CrossAxisAlignment.END),
            ], expand=True, spacing=10),
            expand=True,
            padding=0,
            border_radius=0,
            bgcolor=ft.Colors.WHITE,
        )
    )

ft.app(target=main)