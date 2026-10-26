# CHATBOT BÁSICO

import random
import re
import unicodedata
from pathlib import Path
from typing import Dict, List

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from iagenerativa import generar_respuestas

app = FastAPI(title="Chatbot Cenigraf", version="1.0.0")

# Ruta de la carpeta donde se encuentra chatbot.py
CARPETA = Path(__file__).resolve().parent


# MODELOS DE DATOS DE LA API
class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
    history: List[Dict[str, str]] = Field(default_factory=list)


class ChatResponse(BaseModel):
    reply: str


# FUNCIÓN PARA QUITAR TILDES
def quitar_tildes(texto: str) -> str:
    texto = unicodedata.normalize("NFD", texto)

    texto = "".join(
        caracter
        for caracter in texto
        if unicodedata.category(caracter) != "Mn"
    )

    return texto


# FUNCIÓN PARA LEER LA OFERTA EDUCATIVA
def leer_ofertas_educativas() -> str:
    ruta = CARPETA / "datos.txt"

    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            return archivo.read().strip()

    except FileNotFoundError:
        return "Error: no se encuentra el archivo ofertas_educativas.txt."


""" # FUNCIÓN PRINCIPAL DEL CHATBOT
def responder(mensaje: str) -> str:

    # 1. Leer los datos de aprendizaje
    ruta_datos = CARPETA / "datos.txt"

    try:
        with open(ruta_datos, "r", encoding="utf-8") as archivo:
            lineas = archivo.readlines()

    except FileNotFoundError:
        return "Error: no se encuentra el archivo datos.txt."

    # 2. Construir el diccionario modelo
    modelo = {}

    for linea in lineas:
        palabras = quitar_tildes(linea.strip().lower()).split()

        for i in range(len(palabras) - 1):
            actual = palabras[i]
            siguiente = palabras[i + 1]

            if actual not in modelo:
                modelo[actual] = []

            modelo[actual].append(siguiente)

    # Mostrar el modelo en la terminal
    print("\n=== MODELO CONSTRUIDO ===")

    for palabra, siguientes in modelo.items():
        print(palabra, "->", siguientes)

    # 3. Normalizar el mensaje del usuario
    texto = quitar_tildes(mensaje.strip().lower())

    if not texto:
        return "Por favor, escribe un mensaje."

    palabras_usuario = re.findall(r"\w+", texto)

    # 4. Saludos
    if any(
        palabra in palabras_usuario
        for palabra in ("hola", "buenas", "hey", "ola", "alo")
    ):
        return "¡Hola! ¿Cómo estás? ¡Cuéntame tus ideas o inquietudes!"

    # 5. Identidad del chatbot
    if any(
        frase in texto
        for frase in ("quien eres", "como te llamas")
    ):
        return "Soy tu chatbot especializado para ti."

    # 6. Despedidas
    if any(
        palabra in palabras_usuario
        for palabra in ("adios", "chao", "bye", "chaito")
    ) or "hasta luego" in texto or "nos vemos" in texto:
        return "¡Hasta luego! Si me necesitas, aquí estaré."

    # 7. Ayuda
    if "ayuda" in palabras_usuario:
        return "¿Qué necesitas? Puedo responder preguntas básicas."


    # 8. Oferta educativa, programas y fechas de inscripción
    preguntas_educativas = (
        "oferta educativa",
        "educacion",
        "programas educativos",
        "programas de formacion",
        "programas del sena",
        "que programas hay",
        "que programas educativos hay",
        "hablame sobre la educacion",
        "hablame de la educacion",
        "fechas de inscripcion",
        "fecha de inscripcion",
        "cuando abren las inscripciones",
        "cuando cierran las inscripciones",
        "requisitos de inscripcion",
        "como me inscribo",
        "como inscribirme",
        "inscripciones del sena",
    )

    if any(frase in texto for frase in preguntas_educativas):
        return leer_ofertas_educativas()

    # 10. Diferencia entre técnico y tecnólogo
    if (
        "diferencia" in texto
        and "tecnico" in texto
        and "tecnologo" in texto
    ):
        return (
            "La formación técnica se enfoca en competencias prácticas "
            "para realizar funciones específicas. La formación "
            "tecnológica profundiza en el análisis, la aplicación de "
            "conocimientos y la gestión de procesos. Los alcances "
            "concretos dependen del programa."
        )

    # 11. Preguntas sobre técnicos
    preguntas_tecnico = (
        "que es tecnico",
        "que es un tecnico",
        "que hace un tecnico",
        "que son los tecnicos",
        "el tecnico",
        "los tecnicos",
        "como es el tecnico",
    )

    if any(frase in texto for frase in preguntas_tecnico):
        return (
            "Los programas técnicos desarrollan competencias prácticas "
            "para desempeñar funciones específicas en el entorno laboral. "
            "Consulta la ficha del programa para conocer sus requisitos "
            "y características."
        )

    # 12. Preguntas sobre tecnólogos
    preguntas_tecnologo = (
        "que es tecnologo",
        "que es un tecnologo",
        "que hace un tecnologo",
        "que son los tecnologos",
        "el tecnologo",
        "los tecnologos",
        "como es el tecnologo",
    )

    if any(frase in texto for frase in preguntas_tecnologo):
        return (
            "Los programas tecnológicos desarrollan competencias para "
            "analizar situaciones, aplicar conocimientos y gestionar "
            "procesos en un área profesional. Consulta la ficha del "
            "programa para conocer sus requisitos y características."
        )

    # 13. Tipos de formación
    if any(
        frase in texto
        for frase in (
            "tipos de programa",
            "tipos de formacion",
            "tipo de programa",
            "que tipos de formacion hay",
            "que tipos de programas hay",
        )
    ):
        return (
            "La oferta puede incluir programas técnicos, tecnológicos "
            "y cursos de formación complementaria. Los programas "
            "disponibles dependen de cada convocatoria."
        )

    # 14. Seleccionar palabras conocidas del mensaje
    palabras_vacias = {
        "que", "como", "es", "el", "la", "los", "las",
        "un", "una", "de", "del", "en", "y", "a", "me",
        "puedes", "dime", "sobre", "por", "favor", "cual",
        "cuales", "son", "hay", "cuando", "para", "con",
        "quiero", "saber", "explicame", "hablame",
    }

    candidatas = [
        palabra
        for palabra in palabras_usuario
        if palabra in modelo and palabra not in palabras_vacias
    ]

    # 15. Si no encuentra palabras conocidas
    if not candidatas:
        return (
            "No encuentro una palabra conocida en tu consulta. "
            "Prueba con palabras de mis datos de aprendizaje, como "
            "aprendiz, estudiante, python, flask, react o mysql."
        )

    # 16. Generar una frase usando el modelo
    actual = candidatas[-1]
    frase_generada = [actual]

    for _ in range(7):
        siguientes = modelo.get(actual, [])

        if not siguientes:
            break

        siguiente = random.choice(siguientes)
        frase_generada.append(siguiente)
        actual = siguiente

    # 17. Devolver la respuesta generada
    respuesta = " ".join(frase_generada)

    print("\n=== RESPUESTA GENERADA ===")
    print(respuesta)

    return "Según los patrones de mis datos: " + respuesta """


# RUTA PRINCIPAL
@app.get("/", response_class=HTMLResponse)
def pagina():
    return HTML


# COMPROBAR SI LA API FUNCIONA
@app.get("/api/health")
def health():
    return {"status": "ok"}


# RECIBIR MENSAJES DEL CHAT

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    respuesta = await generar_respuestas(request.message)
    return ChatResponse(reply=respuesta)


# PÁGINA WEB DEL CHATBOT
HTML = r"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CHATBOT BÁSICO</title>

    <style>
        
:root {
    --primario: #0756a4;
    --primario-oscuro: #063b73;
    --secundario: #13a89e;
    --fondo: #eef3f9;
    --blanco: #ffffff;
    --texto: #1c2938;
    --texto-suave: #68778a;
    --borde: #e1e8f0;
    --sombra: 0 12px 40px rgba(15, 45, 80, 0.12);
}

* {
    box-sizing: border-box;
}

body {
    font-family: "Segoe UI", Arial, sans-serif;
    max-width: 820px;
    min-height: 100vh;
    margin: 0 auto;
    padding: 35px 18px;
    background:
        radial-gradient(circle at top left, #d8eaff, transparent 42%),
        var(--fondo);
    color: var(--texto);
}

/* ENCABEZADO */

h1 {
    text-align: center;
    color: var(--primario-oscuro);
    font-size: clamp(25px, 5vw, 35px);
    font-weight: 800;
    letter-spacing: -0.8px;
    margin: 10px 0 8px;
}

h1::after {
    content: "";
    display: block;
    width: 65px;
    height: 4px;
    margin: 14px auto 22px;
    border-radius: 10px;
    background: var(--secundario);
}

/* VENTANA DEL CHAT */

#chat {
    background: rgba(255, 255, 255, 0.96);
    border: 1px solid var(--borde);
    border-radius: 22px;
    padding: 24px 18px;
    min-height: 400px;
    max-height: 58vh;
    overflow-y: auto;
    overflow-wrap: anywhere;
    box-shadow: var(--sombra);
    scroll-behavior: smooth;
}

/* BARRA DE DESPLAZAMIENTO */

#chat::-webkit-scrollbar {
    width: 7px;
}

#chat::-webkit-scrollbar-thumb {
    background: #c5d5e7;
    border-radius: 10px;
}

#chat::-webkit-scrollbar-track {
    background: transparent;
}

/* MENSAJES */

.mensaje {
    width: fit-content;
    max-width: 88%;
    padding: 13px 16px;
    margin: 14px 0;
    border-radius: 16px;
    line-height: 1.6;
    font-size: 15px;
    white-space: pre-wrap;
    overflow-wrap: anywhere;
    animation: aparecer 0.25s ease-out;
}

/* PRIMER MENSAJE DE BIENVENIDA */

#chat > .mensaje:first-child {
    background: #e9f4ff;
    color: var(--primario-oscuro);
    border: 1px solid #d6eaff;
    border-radius: 16px;
}

/* FORMULARIO DE ENVÍO */

form {
    display: flex;
    gap: 10px;
    margin-top: 18px;
    padding: 9px;
    background: var(--blanco);
    border: 1px solid var(--borde);
    border-radius: 17px;
    box-shadow: 0 5px 20px rgba(15, 45, 80, 0.06);
}

input {
    flex: 1;
    min-width: 0;
    padding: 13px 14px;
    border: 2px solid transparent;
    border-radius: 11px;
    background: #f5f8fc;
    color: var(--texto);
    font-size: 15px;
    outline: none;
    transition: border-color 0.2s, background 0.2s;
}

input::placeholder {
    color: #8997a8;
}

input:focus {
    background: var(--blanco);
    border-color: var(--primario);
}

/* BOTÓN ENVIAR */

button {
    padding: 0 23px;
    border: none;
    border-radius: 12px;
    background: linear-gradient(
        135deg,
        var(--primario),
        var(--primario-oscuro)
    );
    color: var(--blanco);
    font-size: 15px;
    font-weight: 700;
    cursor: pointer;
    box-shadow: 0 4px 12px rgba(7, 86, 164, 0.2);
    transition: transform 0.2s, box-shadow 0.2s;
}

button:hover {
    transform: translateY(-2px);
    box-shadow: 0 7px 18px rgba(7, 86, 164, 0.28);
}

button:active {
    transform: scale(0.97);
}

button:focus-visible {
    outline: 3px solid var(--secundario);
    outline-offset: 3px;
}

/* ANIMACIÓN */

@keyframes aparecer {
    from {
        opacity: 0;
        transform: translateY(7px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* ADAPTACIÓN A CELULARES */

@media (max-width: 600px) {
    body {
        padding: 20px 12px;
    }

    h1 {
        margin-top: 12px;
    }

    #chat {
        min-height: 50vh;
        max-height: 60vh;
        padding: 16px 12px;
        border-radius: 17px;
    }

    .mensaje {
        max-width: 94%;
        font-size: 14px;
        padding: 11px 13px;
    }

    form {
        gap: 7px;
        padding: 6px;
    }

    input {
        padding: 12px 10px;
        font-size: 14px;
    }

    button {
        padding: 0 15px;
        font-size: 14px;
    }
}

@media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
        animation-duration: 0.01ms !important;
        transition-duration: 0.01ms !important;
        scroll-behavior: auto !important;
    }
}

    </style>
</head>

<body>
    <h1>CHATBOT CENIGRAF</h1>

    <div id="chat" aria-live="polite">
        <p class="mensaje">¡BIENVENIDO A CHATBOT CENIGRAF</p>
    </div>

    <form id="formulario">
        <input
            id="mensaje"
            type="text"
            placeholder="Escribe tu pregunta..."
            maxlength="2000"
            autocomplete="off"
            required
        >
        <button type="submit">Enviar</button>
    </form>

    <script>
        const chat = document.getElementById("chat");
        const formulario = document.getElementById("formulario");
        const entrada = document.getElementById("mensaje");

        function agregarMensaje(remitente, texto) {
            const parrafo = document.createElement("p");
            parrafo.className = "mensaje";
            parrafo.textContent = remitente + ": " + texto;
            chat.appendChild(parrafo);
            chat.scrollTop = chat.scrollHeight;
        }

        formulario.addEventListener("submit", async function(evento) {
            evento.preventDefault();

            const mensaje = entrada.value.trim();

            if (!mensaje) {
                return;
            }

            agregarMensaje("Tú", mensaje);
            entrada.value = "";

            try {
                const respuesta = await fetch("/api/chat", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        message: mensaje
                    })
                });

                if (!respuesta.ok) {
                    throw new Error("No se pudo obtener una respuesta.");
                }

                const datos = await respuesta.json();
                agregarMensaje("Bot", datos.reply);

            } catch (error) {
                agregarMensaje("Bot", "Error: " + error.message);
            }
        });
    </script>
</body>
</html>"""