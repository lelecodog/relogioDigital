# Relógio Mundial

Este é um projeto de Relógio Mundial desenvolvido para aprimorar os estudos de uso de API e a utilização de programação assíncrona (async) em Python. O projeto utiliza a biblioteca Flet para criar a interface gráfica e a API do OpenWeatherMap para obter informações meteorológicas.

## Funcionalidades

- Exibe a hora atual do PC.
- Permite a entrada do nome de uma cidade para obter informações meteorológicas.
- Atualiza a hora e as informações meteorológicas em tempo real.

## Tecnologias Utilizadas

- Python
- Flet
- Requests
- Python-Decouple
- Pytz
- Asyncio

## Instalação

1. Clone o repositório:

git clone <https://github.com/lelecodog/relogioDigital.git>
cd RelogioMundial

2. Crie um ambiente virtual e ative-o:

python -m venv venv
venv\Scripts\activate  # No Windows
source venv/bin/activate  # No macOS/Linux

3. Instale as dependências:

pip install -r requirements.txt

4. Crie um arquivo `.env` na raiz do projeto e adicione sua chave de API do OpenWeatherMap:

API_KEY=sua_openweathermap_api_key

## Utilização

Execute o script `main.py` para iniciar o aplicativo:

python main.py

## Explicação sobre a Utilização do Async

A programação assíncrona (async) é utilizada neste projeto para atualizar a hora e as informações meteorológicas em tempo real sem bloquear a interface do usuário. A função `update_clock` é uma função assíncrona que atualiza a hora a cada segundo. A função `main` cria uma tarefa assíncrona para `update_clock`, permitindo que a interface do usuário continue responsiva enquanto a hora é atualizada em segundo plano.

```python
async def update_clock(label_time, label_info, page):
    global time_zone_global, city_global
    while True:
        now = datetime.now(time_zone_global) if time_zone_global else datetime.now()
        label_time.value = now.strftime("%H:%M:%S")
        label_info.value = f"Time in {city_global}" if city_global else now.strftime("%A, %d %B %Y")
        page.update()
        await asyncio.sleep(1)

async def main(page: ft.Page):
    # Configuração da página e interface
    ...

    # Inicia a tarefa assíncrona do relógio
    asyncio.create_task(update_clock(label_time, label_info, page))

ft.app(target=main)
```

## Contribuição

Sinta-se à vontade para contribuir com melhorias para este projeto. Para contribuir, siga os passos abaixo:

1. Faça um fork do repositório.
2. Crie uma nova branch (`git checkout -b feature/nova-funcionalidade`).
3. Faça commit das suas alterações (`git commit -m 'Adiciona nova funcionalidade'`).
4. Faça push para a branch (`git push origin feature/nova-funcionalidade`).
5. Abra um Pull Request.

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.


