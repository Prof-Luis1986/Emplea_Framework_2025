import flet as ft
from flet_audio import Audio
import os
import threading

def main(page: ft.Page):
    page.title = "Piano Makey Makey"
    page.bgcolor = "black"
    page.window_width = 800
    page.window_height = 400
    page.window_resizable = False
    page.padding = 0
    page.spacing = 0

    base_path = os.path.dirname(__file__)

    image_base_path = os.path.join(base_path, "assets", "Teclado.png")
    teclado_base = ft.Image(src=image_base_path, width=800, height=300)
    page.add(teclado_base)

    notas = {
        "w": "Do",
        "a": "Re",
        "s": "Mi",
        "d": "Fa",
        "f": "Sol",
        "g": "La",
        " ": "Si",
        "space": "Si",
        "arrowright": "Do2",
    }

    # Pre-cargar audios y agregarlos al overlay
    audio_players = {}
    for nota in set(notas.values()):
        audio_path = os.path.join(base_path, "assets", f"{nota}.wav")
        if os.path.exists(audio_path):
            player = Audio(src=audio_path)
            audio_players[nota] = player
            page.overlay.append(player)
        else:
            print(f"❌ No se encontró audio para: {audio_path}")

    page.update()

    def mostrar_nota_visual(nota):
        nota_img_path = os.path.join(base_path, "assets", f"{nota}.png")
        if os.path.exists(nota_img_path):
            teclado_base.src = nota_img_path
            page.update()
        else:
            print(f"⚠️ No se encontró imagen para la nota: {nota_img_path}")

        def reset_visual():
            teclado_base.src = image_base_path
            page.update()

        threading.Timer(0.3, reset_visual).start()

    def on_key(e: ft.KeyboardEvent):
        tecla = e.key.lower()
        print(f"Presionaste: '{tecla}'")

        if tecla in notas:
            nombre_nota = notas[tecla]
            if nombre_nota in audio_players:
                audio_players[nombre_nota].play()
                mostrar_nota_visual(nombre_nota)
            else:
                print(f"❌ Audio no cargado para: {nombre_nota}")
        else:
            print(f"Ignorado: '{tecla}'")

    page.on_keyboard_event = on_key
    page.update()

ft.app(target=main)