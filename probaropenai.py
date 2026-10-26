from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "No se encontro GEMINI_API_KEY en el archivo .env"
    )

cliente = genai.Client(api_key=api_key)

respuesta = cliente.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents="Explica en español:¿que es la inteligencia artificial"
)
print(respuesta.text)