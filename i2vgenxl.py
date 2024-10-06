import replicate
import requests

def upload_image(image_path):
    with open(image_path, 'rb') as img_file:
        response = requests.post(
            "https://freeimage.host/api/1/upload",
            data={
                "key": os.environ["FREEIMAGE_KEY"],
                "action": "upload"
            },
            files={"source": img_file}
        )
        response_data = response.json()
        return response_data['image']['url'] if response.status_code == 200 else None

def i2vgenxl(prompt, image_path):
    image_url = upload_image(image_path)
    
    if image_url:
        output = replicate.run(
            "ali-vilab/i2vgen-xl:5821a338d00033abaaba89080a17eb8783d9a17ed710a6b4246a18e0900ccad4",
            input={
                "image": image_url,
                "prompt": prompt,
                "max_frames": 16,
                "guidance_scale": 9,
                "num_inference_steps": 100
            }
        )
        return output
    else:
        print("Erro ao fazer upload da imagem")
