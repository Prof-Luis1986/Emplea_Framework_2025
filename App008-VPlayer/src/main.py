import flet as ft
import flet_video as fv


def main(page: ft.Page):
    page.title = "VideoPlayer"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.always_on_top = True
    page.spacing = 10
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding =10  # Elimina bordes blancos

    video_data = [
        {"title": "Video 1: Naturaleza", "url": "https://user-images.githubusercontent.com/28951144/229373720-14d69157-1a56-4a78-a2f4-d7a134d7c3e9.mp4"},
        {"title": "Video 2: Ciudad", "url": "https://user-images.githubusercontent.com/28951144/229373718-86ce5e1d-d195-45d5-baa6-ef94041d0b90.mp4"},
        {"title": "Video 3: Espacio", "url": "https://user-images.githubusercontent.com/28951144/229373716-76da0a4e-225a-44e4-9ee7-3e9006dbc3e3.mp4"},
        {"title": "Video 4: Animación", "url": "https://user-images.githubusercontent.com/28951144/229373695-22f88f13-d18f-4288-9bf1-c3e078d83722.mp4"},
        {"title": "Video 5: Música", "url": "https://user-images.githubusercontent.com/28951144/229373709-603a7a89-2105-4e1b-a5a5-a6c3567c9a59.mp4"},
    ]

    playlist = [fv.VideoMedia(item["url"]) for item in video_data]

    current_index = ft.Ref[int]()
    current_index.current = 0

    current_title = ft.Text(video_data[0]["title"], style="titleLarge", text_align=ft.TextAlign.CENTER)

    snackbar = ft.SnackBar(content=ft.Text(""))

    video = fv.Video(
        expand=True,
        playlist=playlist,
        playlist_mode=fv.PlaylistMode.LOOP,
        aspect_ratio=16 / 9,
        volume=100,
        autoplay=False,
        muted=False,
        fill_color=ft.Colors.BLUE_400,
        filter_quality=ft.FilterQuality.HIGH,
        on_loaded=lambda e: print("Video cargado correctamente."),
    )

    def handle_play(e):
        video.play()

    def handle_pause(e):
        video.pause()

    def handle_next(e):
        next_index = (current_index.current + 1) % len(video_data)
        current_index.current = next_index
        video.next()
        current_title.value = video_data[next_index]["title"]
        page.update()

    def handle_previous(e):
        prev_index = (current_index.current - 1) % len(video_data)
        current_index.current = prev_index
        video.previous()
        current_title.value = video_data[prev_index]["title"]
        page.update()

    def handle_volume_change(e):
        video.volume = int(e.control.value)
        video.pause()
        video.play()
        snackbar.content.value = f"🔊 Volumen: {video.volume}%"
        page.snack_bar = snackbar
        page.snack_bar.open = True
        page.update()

    def handle_playback_rate_change(e):
        video.playback_rate = float(e.control.value)
        video.pause()
        video.play()
        snackbar.content.value = f"⏩ Velocidad: {video.playback_rate}x"
        page.snack_bar = snackbar
        page.snack_bar.open = True
        page.update()

    # UI: controles redondeados
    def rounded_button(text, handler):
        return ft.ElevatedButton(
            text,
            on_click=handler,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=20),
                padding=20,
            )
        )

    controls = ft.Row(
        wrap=True,
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10,
        controls=[
            rounded_button("Play", handle_play),
            rounded_button("Pause", handle_pause),
            rounded_button("Previous", handle_previous),
            rounded_button("Next", handle_next),
        ]
    )

    sliders = ft.Column([
        ft.Slider(
            min=0,
            value=100,
            max=100,
            divisions=10,
            width=400,
            label="Volumen = {value}%",
            on_change=handle_volume_change
        ),
        ft.Slider(
            min=0.5,
            value=1,
            max=2,
            divisions=6,
            width=400,
            label="Velocidad = {value}x",
            on_change=handle_playback_rate_change
        )
    ])

    page.add(
        ft.Container(
            expand=True,
            padding=0,
            margin=0,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[ft.Colors.LIGHT_BLUE_100, ft.Colors.BLUE_700],
            ),
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=25,
                controls=[
                    current_title,
                    video,
                    controls,
                    sliders
                ]
            )
        )
    )


ft.app(target=main)
