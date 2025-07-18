import flet as ft
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Preguntas y respuestas ampliadas (con variantes para mejorar el modelo)
preguntas = [
    "hola", "holaa", "buenos días", "buenas tardes", "buenas noches", "buenas",
    "¿cómo estás?", "cómo estás", "qué tal", "¿qué tal?", "¿quién eres?", "quién eres",
    "¿cómo te llamas?", "cómo te llamas", "¿qué es python?", "qué es python",
    "cuéntame un chiste", "dime un chiste", "gracias", "muchas gracias",
    "¿qué tiempo hace?", "¿va a llover?", "¿me puedes ayudar?", "ayuda",
    "¿qué hora es?", "¿qué día es hoy?", "¿puedes aprender?", "¿eres inteligente?",
    "¿cuál es tu color favorito?", "¿te gusta la música?", "¿puedes cantar?",
    "¿puedes bailar?", "¿cuál es tu comida favorita?", "¿puedes contar hasta 10?",
    "cuéntame algo interesante", "adiós", "hasta luego", "nos vemos"
]

respuestas = [
    "¡Hola! ¿En qué puedo ayudarte?",
    "¡Hola! ¿En qué puedo ayudarte?",
    "¡Buenos días! ¿Cómo puedo ayudarte?",
    "¡Buenas tardes! ¿En qué te ayudo?",
    "¡Buenas noches! ¿Necesitas algo?",
    "¡Hola! ¿En qué puedo ayudarte?",
    "¡Estoy bien, gracias! ¿Y tú?",
    "¡Estoy bien, gracias! ¿Y tú?",
    "¡Todo bien! ¿Y tú?",
    "¡Todo bien! ¿Y tú?",
    "Soy tu asistente virtual, creado con Python y un poco de IA.",
    "Soy tu asistente virtual, creado con Python y un poco de IA.",
    "Me llamo Asistente Virtual, pero puedes ponerme el nombre que quieras.",
    "Me llamo Asistente Virtual, pero puedes ponerme el nombre que quieras.",
    "Python es un lenguaje de programación muy popular y fácil de aprender.",
    "Python es un lenguaje de programación muy popular y fácil de aprender.",
    "¿Por qué los programadores confunden Halloween y Navidad? Porque OCT 31 == DEC 25.",
    "¿Por qué el libro de matemáticas estaba triste? Porque tenía demasiados problemas.",
    "¡De nada! Estoy aquí para ayudarte.",
    "¡Gracias a ti por usarme!",
    "No tengo acceso al clima en tiempo real, pero espero que haga buen día.",
    "No puedo predecir el clima, pero lleva paraguas por si acaso.",
    "¡Por supuesto! Pregúntame lo que quieras.",
    "Estoy aquí para ayudarte. ¿Qué necesitas?",
    "No tengo reloj, pero puedes verlo en tu dispositivo.",
    "No tengo calendario, pero seguro que es un gran día.",
    "Por ahora no aprendo, pero puedo responder lo que sé.",
    "¡Intento serlo! ¿Tú qué opinas?",
    "Me gustan todos los colores, pero el azul es especial.",
    "¡Sí! La música alegra el día.",
    "No puedo cantar, pero puedo escribir letras.",
    "No tengo cuerpo, pero bailo en la nube.",
    "No como, pero me gustan los bytes.",
    "¡Claro! Uno, dos, tres, cuatro, cinco, seis, siete, ocho, nueve, diez.",
    "¿Sabías que las abejas pueden reconocer rostros humanos? ¡Increíble!",
    "¡Adiós! Que tengas un buen día.",
    "¡Hasta luego! Vuelve cuando quieras.",
    "¡Nos vemos pronto! Cuídate."
]

# Entrenamiento del modelo
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(preguntas)
modelo = MultinomialNB()
modelo.fit(X, range(len(respuestas)))

def responder(mensaje: str) -> str:
    """Devuelve la respuesta más probable para un mensaje dado."""
    X_test = vectorizer.transform([mensaje])
    idx = modelo.predict(X_test)[0]
    return respuestas[idx]

def main(page: ft.Page):
    page.title = "Asistente Virtual"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = ft.Colors.BLUE_GREY_900

    chat = ft.ListView(
        expand=True,
        spacing=10,
        padding=10,
        auto_scroll=True,
    )

    input_box = ft.TextField(
        hint_text="Escribe tu mensaje...",
        autofocus=True,
        expand=True,
        border_radius=20,
        filled=True,
        bgcolor=ft.Colors.BLUE_GREY_800,
        color=ft.Colors.WHITE,
        on_submit=lambda e: enviar()
    )

    def burbuja(mensaje, es_usuario):
        return ft.Row(
            [
                ft.Container(
                    content=ft.Text(
                        mensaje,
                        color=ft.Colors.WHITE if es_usuario else ft.Colors.BLACK,
                        selectable=True,
                    ),
                    padding=12,
                    bgcolor=ft.Colors.BLUE_700 if es_usuario else ft.Colors.GREY_200,
                    border_radius=20,
                    alignment=ft.alignment.center_right if es_usuario else ft.alignment.center_left,
                    margin=ft.margin.only(left=40) if es_usuario else ft.margin.only(right=40),
                    width=350,
                )
            ],
            alignment=ft.MainAxisAlignment.END if es_usuario else ft.MainAxisAlignment.START,
        )

    def enviar():
        user_msg = input_box.value.strip()
        if not user_msg:
            return
        chat.controls.append(burbuja(f"🧑 {user_msg}", True))
        bot_msg = responder(user_msg.lower())
        chat.controls.append(burbuja(f"🤖 {bot_msg}", False))
        input_box.value = ""
        page.update()

    # Mensaje de bienvenida
    chat.controls.append(burbuja("🤖 ¡Hola! Soy tu asistente virtual. ¿En qué puedo ayudarte?", False))

    # Interfaz principal
    page.add(
        ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.SMART_TOY, size=40, color=ft.Colors.BLUE_400),
                            ft.Text("Asistente Virtual", size=28, weight="bold", color=ft.Colors.BLUE_100),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Container(
                        chat,
                        expand=True,
                        height=450,
                        bgcolor=ft.Colors.BLUE_GREY_800,
                        border_radius=15,
                        padding=10,
                        margin=ft.margin.only(top=10, bottom=10),
                    ),
                    ft.Row(
                        [
                            input_box,
                            ft.IconButton(
                                icon=ft.Icons.SEND,
                                icon_color=ft.Colors.BLUE_400,
                                tooltip="Enviar",
                                on_click=lambda e: enviar(),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                expand=True,
                spacing=10,
            ),
            width=500,
            padding=20,
            border_radius=20,
            bgcolor=ft.Colors.BLUE_GREY_800,
            alignment=ft.alignment.center,
        )
    )

ft.app(target=main)