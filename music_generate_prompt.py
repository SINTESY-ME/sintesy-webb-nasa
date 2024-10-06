import os
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def upload_to_gemini(path, mime_type=None):
  """Uploads the given file to Gemini.

  See https://ai.google.dev/gemini-api/docs/prompting_with_media
  """
  file = genai.upload_file(path, mime_type=mime_type)
  print(f"Uploaded file '{file.display_name}' as: {file.uri}")
  return file

def generate_prompt_from_image(image_path):
    generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    )
    
    files = [
    upload_to_gemini(image_path, mime_type="image/jpeg"),
    ]

    chat_session = model.start_chat(
    history=[
        {
        "role": "user",
        "parts": [
            files[0],
        ],
        },
    ]
    )
    response = chat_session.send_message("""analyze image and define what style inspiration it conveys and what musical style goes with it. create me a prompt for a violin song, name an author or song for inspiration, name instruments or sounds that refer to the image, time signature. all elements must be inspired by the image. maximum 100 words, not markdown. return only the prompt nothing else
    """)
    return response.text
