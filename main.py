import asyncio
from fasthtml.common import *
import uvicorn
import threading
from db import db
from tinydb import Query


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
    
    def card_3d(text, background, amt, left_align, item):
        # JS e CSS podem ser definidos inline ou em um arquivo
        scr = ScriptX('card3d.js', amt=amt)
        align = 'left' if left_align else 'right'
        
        # CSS para centralizar o botão dentro do card, ajustando a imagem PNG
        button_css = """
            display: flex;
            justify-content: center;
            align-items: center;
            width: 20px;
            height: 20px;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background-image: url('https://www.gov.br/pt-br/midias-agorabrasil/play.png/@@images/image.png');
            background-size: contain;
            background-position: center;  /* Centraliza a imagem no botão */
            background-repeat: no-repeat;
            background-color: #ffffff00;
            border: none;
        """
        
        sty = StyleX('card3d.css', background=f'url({background})', align=align)
        
        # O botão agora redireciona para a rota /play, passando o nome da imagem como parâmetro
        return Div(A(Button(id='PREI', style=button_css), href=f'/play?name={item["image_name"]}'), text, Div(), sty, scr)

    # Criação de múltiplos cards
    cards = []
    for item in db.all():
        if item.get("music_path"):
            cards.append(card_3d(f"", item["gif_path"], amt=1.5, left_align=True, item=item))

    for item in db.all():
        if item.get("music_path"):
            cards.append(card_3d(f"", item["gif_path"], amt=1.5, left_align=True, item=item))

    for item in db.all():
        if item.get("music_path"):
            cards.append(card_3d(f"", item["gif_path"], amt=1.5, left_align=True, item=item))

    # Adiciona a imagem centralizada no início da página
    central_image_style = """
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 20px;
    """
    
    central_image = Img(src="logo.png", style=central_image_style)

    return Div(central_image, *cards, style=cardcss)

# Rota padrão
@rt('/')
def get():
    return Div(card_3d_demo())

# Nova rota para a página de exibição /play
@rt('/play')
def play_page(req):
    # Obtém o parâmetro "name" da URL
    image_name = req.query_params.get('name')

    
    # Busca o item no banco de dados com o nome da imagem
    item = db.get(Query().image_name == image_name)
    
    if not item:
        return Div("Item não encontrado")

    # Cria a página com o fundo de GIF, vídeo e música
    video_style = """
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100%;
        height:500px;
    """
    
    music_tag = f'<audio src="{item["music_path"]}" autoplay loop></audio>'
    video_tag = Video(src=item['video_path'], autoplay=True, controls=True, loop=True, style=video_style)
    
    # Retorna a página com o fundo sendo o gif_path
    return Div(
        NotStr(music_tag),
        video_tag,
        style=f"""
            background-image: url({item['gif_path']});
            background-size: cover;
            width: 100vw;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        """
    )

# Função que será executada a cada 5 segundos
async def tarefa_periodica():
    print("Iniciando a tarefa periódica...")
    while True:
        print("Função executada a cada 5 segundos")
        await asyncio.sleep(5)  # Espera 5 segundos

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
