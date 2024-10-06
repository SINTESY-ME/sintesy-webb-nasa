import os
import requests
from tinydb import Query
from db import db, sort_images
from i2vgenxl import i2vgenxl
from video_to_gif import video_to_gif
from music_generate_prompt import generate_prompt_from_image
from musicgen import musicgen

def process_images(images: list[str]):
    for image in images:
        # Gera o vídeo a partir da imagem usando i2vgenxl
        video_url = i2vgenxl('paralax', 'images/'+image)

        # Define os caminhos para salvar o vídeo e o GIF
        video_folder = 'videos'
        music_folder = 'musics'
        gif_folder = 'gifs'
        os.makedirs(video_folder, exist_ok=True)
        os.makedirs(gif_folder, exist_ok=True)
        os.makedirs(music_folder, exist_ok=True)

        video_path = os.path.join(video_folder, f"{os.path.splitext(image)[0]}.mp4")
        music_path = os.path.join(music_folder, f"{os.path.splitext(image)[0]}.mp3")

        # Faz o download do vídeo

        response = requests.get(video_url)
        if response.status_code == 200:
            with open(video_path, 'wb') as video_file:
                video_file.write(response.content)
            print(f"Vídeo salvo em: {video_path}")
        else:
            print(f"Falha ao baixar o vídeo de {video_url}")
            continue

        # Converte o vídeo para GIF usando video_to_gif
        gif_path = video_to_gif(video_path)
        print(f"GIF salvo em: {gif_path}")

        # Verifica se a imagem já existe no banco de dados
        ImageQuery = Query()
        existing_record = db.get(ImageQuery.image_name == image)

        prompt_for_music = generate_prompt_from_image('images/'+image)
        music = musicgen(prompt_for_music)

        response = requests.get(music)
        if response.status_code == 200:
            with open(music_path, 'wb') as music_file:
                music_file.write(response.content)
            print(f"Vídeo salvo em: {music_path}")
        else:
            print(f"Falha ao baixar o vídeo de {video_url}")
            continue

        # Se já existir, atualiza os caminhos do vídeo e GIF
        if existing_record:
            db.update({'video_path': video_path, 'gif_path': gif_path}, ImageQuery.image_name == image)
            print(f"Registro atualizado no banco de dados para a imagem {image}")
        else:
            # Caso contrário, insere um novo registro
            db.insert({
                'image_name': image,
                'video_path': video_path,
                'gif_path': gif_path,
                'music_path': music_path
            })
            print(f"Novo registro inserido no banco de dados para a imagem {image}")

# Exemplo de uso
images = sort_images(size=10)
if images:
    process_images(images)
