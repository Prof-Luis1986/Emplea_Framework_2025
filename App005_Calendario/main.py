import flet as ft
import datetime
import calendar
from dateutil import relativedelta

class FletCalendar(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.get_current_date()
        self.set_theme()
        
        # Inicializar el contenedor del calendario.
        self.calendar_container = ft.Container(
            width=500, height=450, padding=ft.padding.all(10),
            border=ft.border.all(2, self.border_color),
            border_radius=ft.border_radius.all(10),
            alignment=ft.alignment.top_center
        )
        self.build()  # Construir el calendario.
        self.output = ft.Text()  # Añadir control de salida.
    
    def get_current_date(self):
        """Obtener la fecha actual"""
        today = datetime.datetime.today()
        self.current_month = today.month
        self.current_day = today.day
        self.current_year = today.year
    
    def selected_date(self, e):
        """Fecha seleccionada por el usuario"""
        self.output.value = f"Fecha seleccionada: {e.control.data[1]}/{e.control.data[0]}/{e.control.data[2]}"
        self.output.update()
        
    def set_current_date(self):
        """Establecer el calendario a la fecha actual"""
        self.get_current_date()
        self.build()
        self.calendar_container.update()
        
    def change_month(self, delta):
        """Cambiar al mes siguiente o anterior"""
        current = datetime.date(self.current_year, self.current_month, self.current_day)
        new_month = current + relativedelta.relativedelta(months=delta)
        self.current_year = new_month.year
        self.current_month = new_month.month
        self.current_day = min(self.current_day, calendar.monthrange(new_month.year, new_month.month)[1])
        self.build()
        self.calendar_container.update()
        
    def get_calendar(self):
        """Obtener el calendario del módulo calendar"""
        cal = calendar.HTMLCalendar()
        return cal.monthdayscalendar(self.current_year, self.current_month)
    
    def set_theme(self, border_color=ft.colors.PINK_700, text_color=ft.colors.PINK_50, current_day_color=ft.colors.PINK_200):
        """Establecer el tema del calendario"""
        self.border_color = border_color
        self.text_color = text_color
        self.current_day_color = current_day_color
    
    def build(self):
        """Construir el calendario para Flet"""
        current_calendar = self.get_calendar()
        str_date = f"{calendar.month_name[self.current_month]} {self.current_year}"
        
        date_display = ft.Text(str_date, text_align='center', size=20, color=self.text_color)
        next_button = ft.Container(ft.Text('>', text_align='right', size=20, color=self.text_color), on_click=lambda _: self.change_month(1))
        prev_button = ft.Container(ft.Text('<', text_align='left', size=20, color=self.text_color), on_click=lambda _: self.change_month(-1))
        
        calendar_column = ft.Column([
            ft.Row([prev_button, date_display, next_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER, height=40, expand=False),
            ft.Divider(height=1, thickness=2.0, color=self.border_color),
            ft.Row([ft.Text(day, weight=ft.FontWeight.BOLD, color=self.text_color, width=40, text_align='center') for day in ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]], alignment=ft.MainAxisAlignment.CENTER)
        ], spacing=5, width=500, height=450, alignment=ft.MainAxisAlignment.START, expand=False)
        
        for week in current_calendar:
            week_row = ft.Row(alignment=ft.MainAxisAlignment.CENTER, spacing=5)
            for day in week:
                if day > 0:
                    is_current_day_font = ft.FontWeight.W_300
                    is_current_day_bg = ft.colors.TRANSPARENT
                    display_day = str(day).zfill(2)
                    if day == self.current_day and self.current_month == datetime.datetime.today().month and self.current_year == datetime.datetime.today().year:
                        is_current_day_font = ft.FontWeight.BOLD
                        is_current_day_bg = self.current_day_color
                        
                    day_button = ft.Container(
                        content=ft.Text(display_day, weight=is_current_day_font, color=self.text_color),
                        on_click=self.selected_date, data=(self.current_month, day, self.current_year),
                        width=40, height=40, ink=True, alignment=ft.alignment.center,
                        border_radius=ft.border_radius.all(10),
                        bgcolor=is_current_day_bg
                    )
                else:
                    day_button = ft.Container(width=40, height=40, border_radius=ft.border_radius.all(10))
                week_row.controls.append(day_button)
            calendar_column.controls.append(week_row)
        
        self.calendar_container.content = calendar_column
        return self.calendar_container

def main(page: ft.Page):
    page.title = "Calendario"
    page.bgcolor = "green"
    page.theme = ft.theme.Theme(color_scheme_seed=ft.colors.PINK)
    page.dark_theme = ft.theme.Theme(color_scheme_seed=ft.colors.PINK)

    mycal = FletCalendar(page)
    page.add(mycal, mycal.output)
    page.update()

ft.app(target=main)
