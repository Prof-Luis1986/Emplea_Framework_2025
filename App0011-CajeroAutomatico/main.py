import flet as ft

saldo_i = 1000
saldo_f = saldo_i

def main(page: ft.Page):
    
    page.window_height = 600
    page.window_width = 400
    page.title = "Banco CETIS 50"
    page.padding = 20
    page.bgcolor = "green"
    
    label = ft.Text(value="Bienvenido al Banco CETIS 50", size=20, weight=ft.FontWeight.BOLD)
    page.controls.append(label)
    
    deposit_button = ft.ElevatedButton(
        text="Depositar", 
        on_click=lambda e: deposito(page),
        color=ft.colors.RED,  # Color del texto del botón
        bgcolor=ft.colors.YELLOW_500  # Color de fondo del botón
    )
    page.controls.append(deposit_button)
    
    consult_button = ft.ElevatedButton(
        text="Consultar saldo", 
        on_click=lambda e: consulta(page),
        color=ft.colors.RED,  
        bgcolor=ft.colors.YELLOW_500 
    )
    page.controls.append(consult_button)
    
    withdraw_button = ft.ElevatedButton(
        text="Retirar", 
        on_click=lambda e: retiro(page),
        color=ft.colors.RED,  
        bgcolor=ft.colors.YELLOW_500  
    )
    page.controls.append(withdraw_button)
    
    exit_button = ft.ElevatedButton(
        text="Salir", 
        on_click=lambda e: salir(page),
        color=ft.colors.RED,  
        bgcolor=ft.colors.YELLOW_500  
    )
    page.controls.append(exit_button)
    
    # Agregar imagen
    image_path = "cajero.png"  # Ruta de la imagen
    image = ft.Image(src=image_path, width=400, height=300)  # Ajusta el tamaño según sea necesario
    page.controls.append(image)
    
    page.update()

def deposito(page: ft.Page):
    def on_submit(e):
        global saldo_f
        deposito = int(input_box.value)
        saldo_f += deposito
        dialog.open = False
        page.update()
        page.snack_bar = ft.SnackBar(ft.Text("Deposito Recibido"))
        page.snack_bar.open = True
        page.update()
        
    input_box = ft.TextField(label="Ingrese su deposito", autofocus=True)
    dialog = ft.AlertDialog(
        title=ft.Text("Deposito"),
        content=input_box,
        actions=[
            ft.TextButton("OK", on_click=on_submit)
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        on_dismiss=lambda e: print("Dialogo cerrado")
    )
    page.overlay.append(dialog)
    dialog.open = True
    page.update()

def consulta(page: ft.Page):
    global saldo_f
    def close_dialog(e):
        dialog.open = False
        page.update()

    dialog = ft.AlertDialog(
        title=ft.Text("Consulta de saldo"),
        content=ft.Text(f"El saldo en la cuenta es {saldo_f}"),
        actions=[
            ft.TextButton("OK", on_click=close_dialog)
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    page.overlay.append(dialog)
    dialog.open = True
    page.update()

def retiro(page: ft.Page):
    def on_submit(e):
        global saldo_f
        retiro = int(input_box.value)
        if retiro > saldo_f:
            dialog.open = False
            page.update()
            page.snack_bar = ft.SnackBar(ft.Text("Saldo insuficiente"), bgcolor=ft.colors.RED)
            page.snack_bar.open = True
            page.update()
        else:
            saldo_f -= retiro
            dialog.open = False
            page.update()
            page.snack_bar = ft.SnackBar(ft.Text("Retiro Realizado"))
            page.snack_bar.open = True
            page.update()
            
    input_box = ft.TextField(label="Ingrese la cantidad que desea retirar", autofocus=True)
    dialog = ft.AlertDialog(
        title=ft.Text("Retiro"),
        content=input_box,
        actions=[
            ft.TextButton("OK", on_click=on_submit)
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        on_dismiss=lambda e: print("Dialogo cerrado")
    )
    page.overlay.append(dialog)
    dialog.open = True
    page.update()

def salir(page: ft.Page):
    page.window_close()

ft.app(target=main)
#ft.app(target=main,view=ft.WEB_BROWSER)
