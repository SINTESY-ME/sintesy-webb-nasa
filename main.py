import asyncio
from fasthtml.common import *
import uvicorn
import threading

app, rt = fast_app()
cardcss = "font-family: 'Arial Black', 'Arial Bold', Gadget, sans-serif; perspective: 1500px;"
def card_3d_demo():

    """This is a standalone isolated Python component.

    Behavior and styling is scoped to the component."""

    def card_3d(text, background, amt, left_align):

        # JS and CSS can be defined inline or in a file

        scr = ScriptX('card3d.js', amt=amt)

        align='left' if left_align else 'right'

        sty = StyleX('card3d.css', background=f'url({background})', align=align)

        return Div(text, Div(), sty, scr)

    # Design credit: https://codepen.io/markmiro/pen/wbqMPa

    card = card_3d("Mouseover me", 'output.gif', amt=1.5, left_align=True)

    return Div(card, style=cardcss)

# Função que será executada a cada 5 segundos
async def tarefa_periodica():
    print("Iniciando a tarefa periódica...")
    while True:
        print("Função executada a cada 5 segundos")
        await asyncio.sleep(5)  # Espera 5 segundos

# Rota padrão
@rt('/')
def get():
    return Div(card_3d_demo())

# Função para rodar o servidor FastHTML usando Uvicorn diretamente em uma thread
def start_serve():
    print("Iniciando o servidor...")
    uvicorn.run("main:app", host="0.0.0.0", port=5001, reload=False)  # Desativando reload

# Função para iniciar o servidor em uma thread separada
def run_server_in_thread():
    server_thread = threading.Thread(target=start_serve)
    server_thread.start()

# Função principal para rodar o servidor e a tarefa periódica
async def start_app():
    # Inicia o servidor em uma thread separada
    run_server_in_thread()
    
    # Inicia a tarefa periódica
    await tarefa_periodica()

# Executa o loop de eventos
if __name__ == "__main__":
    asyncio.run(start_app())
