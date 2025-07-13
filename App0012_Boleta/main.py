import flet as ft

def main(page: ft.Page):
    page.title = "Boleta de calificaciones"
    page.bgcolor = "purple"
    page.window_width = 1600
    page.window_height = 600

    # Crear una lista desplegable con los nombres de los alumnos y su etiqueta
    lista_alumnos = ft.Dropdown(
        width=300,
        label="Alumnos",
        options=[
            ft.dropdown.Option("Juan Manuel Martínez"),
            ft.dropdown.Option("María Fernanda Pérez"),
            ft.dropdown.Option("José Luis González"),
            ft.dropdown.Option("Ana María Sánchez"),
            ft.dropdown.Option("Pedro Pérez Pérez"),
        ],
    )
    
    # Crear dropdowns con etiquetas para las materias
    esp = ft.Dropdown(
        width=200,
        label="Español",
        options=[ft.dropdown.Option(str(i)) for i in range(10, 101, 10)]
    )
    
    mat = ft.Dropdown(
        width=200,
        label="Matemáticas",
        options=[ft.dropdown.Option(str(i)) for i in range(10, 101, 10)]
    )

    ing = ft.Dropdown(
        width=200,
        label="Inglés",
        options=[ft.dropdown.Option(str(i)) for i in range(10, 101, 10)]
    )

    info = ft.Dropdown(
        width=300,
        label="Informática",
        options=[ft.dropdown.Option(str(i)) for i in range(10, 101, 10)]
    )

    hist = ft.Dropdown(
        width=200,
        label="Historia",
        options=[ft.dropdown.Option(str(i)) for i in range(10, 101, 10)]
    )

    label_promedio = ft.Text(value="", size=20, width=100, color="white")

    # Crear la tabla
    tabla_calificaciones = ft.DataTable(
        columns=[
            ft.DataColumn(label=ft.Text("Alumno")),
            ft.DataColumn(label=ft.Text("Español")),
            ft.DataColumn(label=ft.Text("Matemáticas")),
            ft.DataColumn(label=ft.Text("Inglés")),
            ft.DataColumn(label=ft.Text("Informática")),
            ft.DataColumn(label=ft.Text("Historia")),
            ft.DataColumn(label=ft.Text("Promedio")),
        ],
        rows=[]
    )

    # Función para calcular el promedio y agregar una fila a la tabla
    def calcular_promedio(e):
        notas = [
            int(esp.value or 0),
            int(mat.value or 0),
            int(ing.value or 0),
            int(info.value or 0),
            int(hist.value or 0)
        ]
        promedio = sum(notas) / len(notas)
        label_promedio.value = f"{promedio:.2f}"
        
        # Agregar una nueva fila a la tabla
        nueva_fila = ft.DataRow(cells=[
            ft.DataCell(ft.Text(lista_alumnos.value or "")),
            ft.DataCell(ft.Text(esp.value or "")),
            ft.DataCell(ft.Text(mat.value or "")),
            ft.DataCell(ft.Text(ing.value or "")),
            ft.DataCell(ft.Text(info.value or "")),
            ft.DataCell(ft.Text(hist.value or "")),
            ft.DataCell(ft.Text(f"{promedio:.2f}")),
        ])
        tabla_calificaciones.rows.append(nueva_fila)
        page.update()

    # Botón para calcular el promedio
    boton_calcular = ft.ElevatedButton(text="Calcular Promedio", on_click=calcular_promedio)

    # Crear filas
    fila_dropdowns = ft.Row(
        [
            lista_alumnos,
            esp,
            mat,
            ing,
            info,
            hist,
            label_promedio
        ],
        alignment=ft.MainAxisAlignment.SPACE_AROUND
    )

    fila_boton = ft.Row(
        [boton_calcular],
        alignment=ft.MainAxisAlignment.CENTER
    )

    # Añadir las filas y la tabla a la página
    page.add(
        ft.Column(
            [
                fila_dropdowns,
                fila_boton,
                tabla_calificaciones
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20
        )
    )

# Iniciar la aplicación con la función 'main' como objetivo
#ft.app(target=main)
ft.app(target=main,view=ft.WEB_BROWSER)
