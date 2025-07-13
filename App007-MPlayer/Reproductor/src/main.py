import flet as ft
from flet_audio import Audio

def main(page: ft.Page):
    page.title = "MediaPlayer"
    page.window_width = 420
    page.window_height = 500
    page.bgcolor = "#181824"

    status = ft.Text("Selecciona archivos MP3", size=16, color="#39FF14", weight="bold")
    file_picker = ft.FilePicker()
    page.overlay.append(file_picker)

    playlist = []
    playlist_view = ft.ListView(expand=True, height=140, spacing=5, padding=10)
    current_index = {"value": -1}
    audio = None  # No se crea hasta que haya canción

    def pick_files(e):
        file_picker.pick_files(allow_multiple=True, allowed_extensions=["mp3"])

    def on_files_selected(e: ft.FilePickerResultEvent):
        nonlocal audio
        if e.files:
            for f in e.files:
                if not any(item.path == f.path for item in playlist):
                    playlist.append(f)
                    idx = len(playlist) - 1
                    playlist_view.controls.append(
                        ft.ListTile(
                            title=ft.Text(f.name, color="#39FF14"),
                            on_click=lambda ev, idx=idx: play_from_playlist(idx),
                        )
                    )
            status.value = f"{len(playlist)} archivos en la playlist"
            # Si es la primera vez, crea el audio con la primera canción
            if audio is None and playlist:
                audio = Audio(src=playlist[0].path, autoplay=False)
                page.controls.insert(0, audio)
                current_index["value"] = 0
                status.value = f"🎵 Reproduciendo: {playlist[0].name}"
                page.update()  # <-- ¡Actualiza la página primero!
                audio.play()   # <-- Ahora sí puedes llamar a play()
            page.update()

    def play_from_playlist(idx):
        if 0 <= idx < len(playlist):
            if audio:
                audio.src = playlist[idx].path
                audio.play()
                status.value = f"🎵 Reproduciendo: {playlist[idx].name}"
                current_index["value"] = idx
                page.update()

    def play_audio(e):
        idx = current_index["value"]
        if idx == -1 and playlist:
            play_from_playlist(0)
        elif audio and audio.src:
            audio.play()
            status.value = f"🎵 Reproduciendo: {playlist[idx].name}"
            page.update()
        else:
            status.value = "¡Selecciona archivos primero!"
            page.update()

    def pause_audio(e):
        if audio:
            audio.pause()
            status.value = "⏸️ Pausado"
            page.update()

    def stop_audio(e):
        if audio:
            audio.pause()
            audio.seek(0)
            status.value = "⏹️ Detenido"
            page.update()

    def next_audio(e):
        idx = current_index["value"]
        if idx + 1 < len(playlist):
            play_from_playlist(idx + 1)

    def prev_audio(e):
        idx = current_index["value"]
        if idx > 0:
            play_from_playlist(idx - 1)

    file_picker.on_result = on_files_selected

    button_style = ft.ButtonStyle(
        bgcolor="#00fff7",
        color="#181824",
        shape=ft.RoundedRectangleBorder(radius=12),
        overlay_color="#39FF14"
    )

    page.add(
        ft.Column([
            ft.Container(
                content=ft.Image(src="Onda.gif", width=120, height=120),
                alignment=ft.alignment.center,
                margin=ft.margin.only(top=10, bottom=10)
            ),
            status,
            ft.ElevatedButton(
                "Agregar MP3s a la Playlist",
                icon=ft.Icons.LIBRARY_MUSIC,
                style=ft.ButtonStyle(
                    bgcolor="#39FF14",
                    color="#181824",
                    shape=ft.RoundedRectangleBorder(radius=12),
                    overlay_color="#00fff7"
                ),
                on_click=pick_files,
                height=45
            ),
            ft.Container(
                playlist_view,
                bgcolor="#22223b",
                border_radius=10,
                padding=10,
                margin=ft.margin.only(top=10, bottom=10)
            ),
            ft.Row([
                ft.ElevatedButton(
                    content=ft.Icon(ft.Icons.SKIP_PREVIOUS, color="#181824"),
                    style=button_style,
                    on_click=prev_audio,
                    height=45,
                    width=45
                ),
                ft.ElevatedButton(
                    content=ft.Icon(ft.Icons.PLAY_ARROW, color="#181824"),
                    style=button_style,
                    on_click=play_audio,
                    height=45,
                    width=45
                ),
                ft.ElevatedButton(
                    content=ft.Icon(ft.Icons.PAUSE, color="#181824"),
                    style=button_style,
                    on_click=pause_audio,
                    height=45,
                    width=45
                ),
                ft.ElevatedButton(
                    content=ft.Icon(ft.Icons.STOP, color="#181824"),
                    style=button_style,
                    on_click=stop_audio,
                    height=45,
                    width=45
                ),
                ft.ElevatedButton(
                    content=ft.Icon(ft.Icons.SKIP_NEXT, color="#181824"),
                    style=button_style,
                    on_click=next_audio,
                    height=45,
                    width=45
                ),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=10)
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=15
        )
    )

ft.app(target=main)