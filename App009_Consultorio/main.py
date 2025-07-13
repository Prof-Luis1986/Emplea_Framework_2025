import flet as ft
import json

def main(page: ft.Page):
    page.title = "Búsqueda de Citas Médicas"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Recuperar citas almacenadas
    stored_citas = page.client_storage.get('citas')  # Corregido: ahora solo se pasa un argumento
    citas = json.loads(stored_citas) if stored_citas else []

    def actualizar_tabla():
        citas_table.rows.clear()
        for cita in citas:
            citas_table.rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(cita['nombre'])),
                ft.DataCell(ft.Text(cita['edad'])),
                ft.DataCell(ft.Text(cita['especialidad'])),
                ft.DataCell(ft.Text(cita['doctor'])),
            ]))
        page.update()

    def guardar_cita(e):
        if nombre.value and edad.value and especialidad.value and doctor.value:
            cita = {
                'nombre': nombre.value,
                'edad': edad.value,
                'especialidad': especialidad.value,
                'doctor': doctor.value
            }
            citas.append(cita)
            page.client_storage.set('citas', json.dumps(citas))
            nombre.value = edad.value = especialidad.value = doctor.value = ''
            page.snack_bar = ft.SnackBar(ft.Text("Cita guardada con éxito!"))
            page.snack_bar.open = True
            actualizar_tabla()
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Por favor complete todos los campos!"), bgcolor=ft.colors.RED)
            page.snack_bar.open = True
            page.update()

    nombre = ft.TextField(label="Nombre", width=300)
    edad = ft.TextField(label="Edad", width=300)
    especialidad = ft.Dropdown(label="Especialidad", width=300, options=[
        ft.dropdown.Option("Pediatría"),
        ft.dropdown.Option("Cardiología"),
        ft.dropdown.Option("Dermatología")
    ])
    doctor = ft.Dropdown(label="Doctor", width=300, options=[
        ft.dropdown.Option("Dr. García"),
        ft.dropdown.Option("Dra. Pérez"),
        ft.dropdown.Option("Dr. Sánchez")
    ])
    guardar_btn = ft.ElevatedButton(text="Guardar Cita", on_click=guardar_cita)

    citas_table = ft.DataTable(columns=[
        ft.DataColumn(label=ft.Text("Nombre")),
        ft.DataColumn(label=ft.Text("Edad")),
        ft.DataColumn(label=ft.Text("Especialidad")),
        ft.DataColumn(label=ft.Text("Doctor")),
    ], rows=[])

    # Inicializa la tabla con las citas guardadas
    actualizar_tabla()

    page.add(
        ft.Column([
            ft.Row([
                ft.Image(src="Consultorio.png", width=100),
                ft.Text("Consultorio Médico", style="color: white; font-size: 24px; font-weight: bold;")
            ], alignment=ft.CrossAxisAlignment.START),
            ft.Divider(),
            nombre,
            edad,
            especialidad,
            doctor,
            guardar_btn,
            ft.Divider(),
            citas_table
        ], alignment=ft.MainAxisAlignment.START)
    )

if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER)
