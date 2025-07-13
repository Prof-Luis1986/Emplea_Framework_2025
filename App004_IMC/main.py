import flet as ft

def calcular_imc(txtPeso, txtAltura, lblIMC, page):
    try:
        peso = float(txtPeso.value.strip())
        altura = float(txtAltura.value.strip())
        imc = peso / (altura * altura)
        lblIMC.value = f"Tu IMC es de: {imc:.2f}"
        page.update()

        # Función para cerrar el cuadro de diálogo y actualizar la página
        def cerrar_dialogo(e):
            page.dialog.open = False
            page.update()

        # Validación del IMC y creación del cuadro de diálogo
        if imc < 18.5:
            dialog = ft.AlertDialog(
                title=ft.Text("Resultado de IMC"),
                content=ft.Text("Actualmente estás bajo de peso"),
                actions=[ft.TextButton("OK", on_click=cerrar_dialogo)],
            )
        elif 18.5 <= imc <= 24.9:
            dialog = ft.AlertDialog(
                title=ft.Text("Resultado de IMC"),
                content=ft.Text("Tu peso es normal"),
                actions=[ft.TextButton("OK", on_click=cerrar_dialogo)],
            )
        elif 25.0 <= imc <= 30.0:
            dialog = ft.AlertDialog(
                title=ft.Text("Resultado de IMC"),
                content=ft.Text("Tienes sobrepeso, debes cuidarte"),
                actions=[ft.TextButton("OK", on_click=cerrar_dialogo)],
            )
        else:
            dialog = ft.AlertDialog(
                title=ft.Text("Resultado de IMC"),
                content=ft.Text("Tienes obesidad, consulta a tu médico"),
                actions=[ft.TextButton("OK", on_click=cerrar_dialogo)],
            )
        page.dialog = dialog
        dialog.open = True
        page.update()
    except ValueError:
        def cerrar_dialogo(e):
            page.dialog.open = False
            page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("Error"),
            content=ft.Text("Los datos ingresados son incorrectos"),
            actions=[ft.TextButton("OK", on_click=cerrar_dialogo)],
        )
        page.dialog = dialog
        dialog.open = True
        page.update()

def main(page: ft.Page):
    # Configuración Básica
    page.title = "Calcular IMC"
    page.bgcolor = "#8408E5"

    # Creación de los componentes de la interfaz
    txtPeso = ft.TextField(label="Ingresa tu peso")
    txtAltura = ft.TextField(label="Ingresa tu altura")
    lblIMC = ft.Text("Tu IMC es de: ")

    # Agrego una imagen (reemplaza la ruta con la correcta)
    img = ft.Image(src="/Users/luismartinezalfaro/Desktop/Ejercicios_Flet/app06_IMC/IMC_app/Bascula.png",
                   width=200,
                   height=200,
                   fit=ft.ImageFit.CONTAIN)

    # Función para el evento de clic en el botón Calcular
    def on_calcular_click(event):
        calcular_imc(txtPeso, txtAltura, lblIMC, page)

    def limpiar(e):
        txtPeso.value=""
        txtAltura.value=""
        lblIMC.value="Tu IMC es de: "
        page.update()

    # Botón para calcular el IMC
    btnCalcular = ft.ElevatedButton(text="Calcular", on_click=on_calcular_click)
    btnLimpiar=ft.ElevatedButton(text="Borrar",on_click=limpiar)

    # Agregar los elementos a la página
    page.add(
        ft.Column(controls=[
            txtPeso, txtAltura, lblIMC
        ], alignment="center"),
        ft.Row(controls=[
            img
        ], alignment="center"),
        ft.Row(controls=[
            btnCalcular,btnLimpiar
        ], alignment="center")
    )

ft.app(target=main)
#ft.app(target=main,view=ft.WEB_BROWSER)