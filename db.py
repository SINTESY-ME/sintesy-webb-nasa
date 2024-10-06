import os
import random
from tinydb import TinyDB, Query

# Inicializa o banco de dados
db = TinyDB('db.json')

def sort_images(image_folder='images', size=5):
    all_images = os.listdir(image_folder)
    ImageQuery = Query()
    stored_images = [item['image_name'] for item in db.all()]
    new_images = list(set(all_images) - set(stored_images))
    
    if not new_images:
        print("Todas as imagens já foram usadas.")
        return None

    size = min(size, len(new_images))
    selected_images = random.sample(new_images, size)

    for image in selected_images:
        db.insert({'image_name': image})
    
    print(f"Imagens selecionadas: {selected_images}")
    return selected_images
