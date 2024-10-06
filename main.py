import asyncio
from fasthtml.common import *
import uvicorn
import threading
from db import db
from tinydb import Query
from process_images import process_images

app, rt = fast_app()
cardcss = """
    font-family: 'Arial Black', 'Arial Bold', Gadget, sans-serif;
    display: grid;
    gap: 0px 50px;
    justify-content: center;
    align-items: center;
    height: 100vh;
    padding: 20px;

    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
"""

def cards():
    
    def card_3d(text, background, amt, left_align, item):
        scr = ScriptX('card3d.js', amt=amt)
        align = 'left' if left_align else 'right'
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
        
        return Div(A(Button(id='PREI', style=button_css), href=f'/play?name={item["image_name"]}'), text, Div(), sty, scr)

    cards = []
    for item in db.all():
        if item.get("video_path"):
            cards.append(card_3d(f"", item["gif_path"], amt=1.5, left_align=True, item=item))

    central_image_style = """
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 20px;
    """
    
    central_image = Img(src="logo.png", style=central_image_style)

    return Div(central_image, *cards, style=cardcss)

@rt('/')
def get():
    background_style = """
        position: fixed;  /* Fixa a div do fundo para não se mover no scroll */
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background-image: url('background.gif');  /* Altere para o caminho do seu GIF */
        background-size: cover;  /* Faz o fundo ocupar toda a tela */
        background-repeat: no-repeat;  /* Não repetir a imagem */
        z-index: -2;  /* Fica atrás de tudo */
    """

    overlay_style = """
        position: fixed;  /* Fixa a div de overlay para não se mover no scroll */
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background-color: rgba(0, 0, 0, 0.5);  /* Camada preta com 50% de opacidade */
        z-index: -1;  /* Fica atrás dos cards */
    """

    cards_style = """
        position: relative;  /* A div dos cards pode se mover normalmente */
        z-index: 1;  /* Fica na frente das outras duas */
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;  /* Alinha os cards em coluna */
    """

    return Div(
        Div(name='background', style=background_style), 
        Div(name='overlay', style=overlay_style), 
        Div(cards(), style=cards_style),
        name='main_container'
    )

@rt('/play')
def play_page(req):
    image_name = req.query_params.get('name')
    item = db.get(Query().image_name == image_name)
    
    if not item:
        return Div("Item não encontrado")

    video_style = """
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100%;
        height:500px;
    """
    music_path = item['video_path'].replace('videos', 'musics')
    music_tag = f'<audio src="{music_path}" autoplay loop></audio>'
    video_tag = Video(src=item['video_path'], autoplay=True, controls=False, loop=True, style=video_style)
    
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

async def tarefa_periodica():
    print("Iniciando a tarefa periódica...")
    while True:
        await asyncio.sleep(86400)
        process_images()

def start_serve():
    print("Iniciando o servidor...")
    uvicorn.run("main:app", host="0.0.0.0", port=5001, reload=False)

def run_server_in_thread():
    server_thread = threading.Thread(target=start_serve)
    server_thread.start()

async def start_app():
    run_server_in_thread()
    await tarefa_periodica()

if __name__ == "__main__":
    asyncio.run(start_app())
