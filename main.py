import flet as ft
import requests
from datetime import datetime
import pytz
import asyncio
from datetime import timezone, timedelta
from decouple import config


COLOR_BG = "#1E1E1E" # Cor de fundo
COLOR_WHITE = "#E0E0E0" # Cor branca texto
COLOR_PRIMARY = "#FF5722" # Cor Laranja
COLOR_SECONDARY = "#757575" # Cor cinza

time_zone_global = None
city_global = None

async def update_clock(label_time, label_info, page):
    global time_zone_global, city_global
    while True:
        now = datetime.now(time_zone_global) if time_zone_global else datetime.now()
        label_time.value = now.strftime("%H:%M:%S")
        label_info.value = f"Time in {city_global}" if city_global else now.strftime("%A, %d %B %Y")
        page.update()
        await asyncio.sleep(1)

def update_weather(e, city_input, Weather_label, label_time, label_info, page):
    global time_zone_global, city_global
    city = city_input.value.strip()

    if not city:
        Weather_label.value = "Digite o nome da cidade"
        time_zone_global, city_global = None, None
        page.update()
        return
    
    api_key = config("API_KEY")

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            #dados da temperatura e descrrição
            temp = data["main"]["temp"]
            description = data["weather"][0]["description"]
            Weather_label.value = f"Temperatura: {temp}°C, {description.capitalize()}"
            
            #atualiza informações globais
            city_global = city

            # Atualiza o fuso horário com base no offset UTC
            utc_offset = data["timezone"]  # Deslocamento UTC em segundos
            time_zone_global = timezone(timedelta(seconds=utc_offset))
            page.update()

        else:
            Weather_label.value = "Cidade não encontrada"


    except requests.exceptions.RequestException:
        Weather_label.value = "Erro ao obter dados da API"
        time_zone_global, city_global = None, None
   
    
async def main(page: ft.Page):
    # configurando a página
    page.title = "Relógio Digital"
    page.window.width = 500
    page.window.height = 530
    page.window.bg_color = COLOR_BG
    page.window.resizable = False

    # configurando interface
    title_label = ft.Text("Relógio Digital", color=COLOR_PRIMARY, size=30, weight="bold")
    label_time = ft.Text("00:00:00", color=COLOR_WHITE, size=50, weight="bold")
    label_info = ft.Text("", color=COLOR_WHITE, size=30)

    city_input = ft.TextField(label="Entre com nome da cidade", text_align="center", bgcolor="#333333", color=COLOR_WHITE, border_radius=8)

    Weather_label = ft.Text("", size=16, color=COLOR_WHITE)

    update_button = ft.ElevatedButton(
        "Atualizar Tempo",
        icon=ft.icons.SEARCH,
        bgcolor=COLOR_PRIMARY,
        color=COLOR_WHITE, 
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        on_click=lambda e: update_weather(e, city_input, Weather_label, label_time, label_info, page),
    )

    

    container = ft.Container(
        ft.Column(
            [
                ft.Icon(name=ft.icons.ACCESS_TIME, size=50, color=COLOR_PRIMARY),
                title_label,
                label_time,
                label_info,
                city_input,
                update_button,
                ft.Icon(name=ft.icons.WB_SUNNY, size=40, color=COLOR_PRIMARY),
                Weather_label,
            ],

            alignment=ft.MainAxisAlignment.CENTER,
            spacing=12,

        ),
        padding=20,
        border_radius=20,
        bgcolor="#2C2C2C",

    )  
    
    page.add(container)

    # inicia a tarefa assincrona do relógio
    asyncio.create_task(update_clock(label_time, label_info, page))

ft.app(target=main)
