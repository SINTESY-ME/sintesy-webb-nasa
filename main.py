import asyncio
from fasthtml.common import *
import uvicorn
import threading

app, rt = fast_app()
cardcss = """
    font-family: 'Arial Black', 'Arial Bold', Gadget, sans-serif;
    perspective: 1500px;
    display: grid;
    grid-template-columns: repeat(6, 1fr); /* 6 colunas na grid */
    grid-gap: 20px;
    justify-content: center;
    align-items: center;
    height: 100vh;
    padding: 20px;
"""

def card_3d_demo():
    """This is a standalone isolated Python component.
    Behavior and styling is scoped to the component."""
    
    def card_3d(text, background, amt, left_align):
        # JS e CSS podem ser definidos inline ou em um arquivo
        scr = ScriptX('card3d.js', amt=amt)
        align = 'left' if left_align else 'right'
        
        # CSS para centralizar o botão dentro do card, ajustando a imagem PNG
        button_css = """
            display: flex;
            justify-content: center;
            align-items: center;
            width: 50px;
            height: 50px;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background-image: url('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSltrgFgRcImcclKMY6j0HnfJw1o_FaLn0FQQ');
            background-size: contain;
            background-position: center;  /* Centraliza a imagem no botão */
            background-repeat: no-repeat;
            background-color: #ffffff00;
            border-radius: 50px;
            border: none;
        """
        
        sty = StyleX('card3d.css', background=f'url({background})', align=align)
        
        return Div(Button(id='PREI', style=button_css), text, Div(), sty, scr)

    # Criação de múltiplos cards
    cards = [
        card_3d(f"Card {i+1}", f"output{i+1}.gif", amt=1.5, left_align=(i % 2 == 0))
        for i in range(20)  # Alterar esse valor para adicionar mais ou menos cards
    ]

    # Retorna os cards em um contêiner com estilo definido
    return Div(*cards, style=cardcss)

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
