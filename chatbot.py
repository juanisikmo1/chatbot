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

.preguntas-frecuentes {
    margin: 20px 0;
    padding: 18px;
    background: #ffffff;
    border: 1px solid #e1e8f0;
    border-radius: 18px;
    box-shadow: 0 5px 20px rgba(15, 45, 80, 0.06);
}

.preguntas-frecuentes h2 {
    margin: 0 0 14px;
    color: #063b73;
    font-size: 18px;
}

.botones-preguntas {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}

.pregunta-btn {
    padding: 10px 14px;
    border: 1px solid #c9def5;
    border-radius: 12px;
    background: #edf5ff;
    color: #0756a4;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    box-shadow: none;
    transition: background 0.2s, color 0.2s;
}

.pregunta-btn:hover {
    background: #0756a4;
    color: #ffffff;
    transform: none;
    box-shadow: none;
}

.pregunta-btn:focus-visible {
    outline: 3px solid #13a89e;
    outline-offset: 3px;
}

@media (max-width: 600px) {
    .botones-preguntas {
        flex-direction: column;
    }

    .pregunta-btn {
        width: 100%;
        text-align: left;
    }
}

.indicador-escribiendo {
    display: flex;
    align-items: center;
    gap: 10px;
    background: #e9f4ff;
    color: #063b73;
    border: 1px solid #d6eaff;
    font-style: italic;
}

/* Respetar el atributo hidden */
.indicador-escribiendo[hidden] {
    display: none !important;
}

/* Puntos animados */
.puntos-animados {
    width: 8px;
    height: 8px;
    flex-shrink: 0;
    border-radius: 50%;
    background: #13a89e;
    animation: pulsar 1s infinite ease-in-out;
}

@keyframes pulsar {
    0%, 100% {
        opacity: 0.3;
        transform: scale(0.8);
    }

    50% {
        opacity: 1;
        transform: scale(1.2);
    }
}

@media (prefers-reduced-motion: reduce) {
    .puntos-animados {
        animation: none;
    }
}

.barra-chat {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    margin: 16px 0;
    padding: 12px 15px;
    background: #ffffff;
    border: 1px solid #e1e8f0;
    border-radius: 14px;
}

.estado-chat {
    color: #68778a;
    font-size: 14px;
}

/* BOTÓN LIMPIAR CHAT */

.boton-limpiar {
    padding: 10px 14px;
    border: 1px solid #d7e0eb;
    border-radius: 10px;
    background: #ffffff;
    color: #b42318;
    font-size: 13px;
    font-weight: 700;
    cursor: pointer;
    box-shadow: none;
}

.boton-limpiar:hover {
    background: #fff1f0;
    border-color: #f2b8b5;
    transform: none;
    box-shadow: none;
}

.boton-limpiar:focus-visible {
    outline: 3px solid #13a89e;
    outline-offset: 3px;
}

@media (max-width: 600px) {
    .barra-chat {
        align-items: flex-start;
        flex-direction: column;
    }

    .boton-limpiar {
        width: 100%;
    }
}
html {
    width: 100%;
    max-width: 100%;
    overflow-x: hidden;
    -webkit-text-size-adjust: 100%;
}

body {
    width: 100%;
    max-width: 820px;
    min-width: 0;
    margin: 0 auto;
    padding: 24px 18px;
    overflow-x: hidden;
}

#chat,
.preguntas-frecuentes,
.barra-chat,
form {
    width: 100%;
    min-width: 0;
    max-width: 100%;
}

#chat {
    max-height: 60vh;
    min-height: 320px;
    overflow-y: auto;
    overflow-x: hidden;
    overflow-wrap: anywhere;
    overscroll-behavior-y: contain;
    -webkit-overflow-scrolling: touch;
}

.mensaje {
    max-width: 100%;
    overflow-wrap: anywhere;
    word-break: normal;
    line-height: 1.65;
}

.botones-preguntas {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}

.pregunta-btn,
.boton-limpiar,
form button {
    min-height: 44px;
    touch-action: manipulation;
}

input {
    min-width: 0;
    width: 100%;
    min-height: 46px;
    font-size: 16px;
}

form {
    align-items: stretch;
}

form button {
    flex-shrink: 0;
}

/* TABLETAS */
@media (max-width: 768px) {
    body {
        padding: 20px 16px;
    }

    h1 {
        font-size: clamp(24px, 5vw, 32px);
    }

    #chat {
        min-height: 300px;
        max-height: 58vh;
        padding: 18px 14px;
    }

    .preguntas-frecuentes {
        padding: 15px;
    }

    .mensaje {
        max-width: 96%;
        font-size: 15px;
    }
}

/* CELULARES */
@media (max-width: 480px) {
    body {
        padding: 14px 10px;
    }

    h1 {
        font-size: 25px;
        letter-spacing: -0.4px;
        margin: 8px 0 16px;
    }

    .barra-chat {
        flex-direction: column;
        align-items: stretch;
        gap: 10px;
        padding: 12px;
        margin: 12px 0;
    }

    .estado-chat {
        font-size: 13px;
    }

    .boton-limpiar {
        width: 100%;
        min-height: 44px;
    }

    .preguntas-frecuentes {
        padding: 13px;
        margin: 14px 0;
        border-radius: 14px;
    }

    .preguntas-frecuentes h2 {
        font-size: 17px;
    }

    .botones-preguntas {
        flex-direction: column;
        gap: 8px;
    }

    .pregunta-btn {
        width: 100%;
        min-height: 46px;
        padding: 11px 12px;
        text-align: left;
        font-size: 14px;
        line-height: 1.4;
    }

    #chat {
        min-height: 280px;
        max-height: 52vh;
        padding: 14px 10px;
        border-radius: 15px;
    }

    .mensaje {
        max-width: 100%;
        padding: 11px 12px;
        margin: 10px 0;
        font-size: 14px;
        line-height: 1.6;
    }

    form {
        display: flex;
        gap: 7px;
        margin-top: 12px;
        padding: 6px;
        border-radius: 13px;
    }

    input {
        flex: 1;
        width: 0;
        min-width: 0;
        padding: 11px 9px;
        font-size: 16px;
    }

    form button {
        min-height: 46px;
        padding: 0 13px;
        font-size: 14px;
    }
}

/* CELULARES MUY ESTRECHOS */
@media (max-width: 350px) {
    body {
        padding: 12px 7px;
    }

    h1 {
        font-size: 22px;
    }

    form {
        gap: 5px;
    }

    form button {
        padding: 0 9px;
    }

    #chat {
        padding: 11px 8px;
    }
}

/* Accesibilidad: respetar preferencias de movimiento */
@media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
        scroll-behavior: auto !important;
        animation-duration: 0.01ms !important;
        transition-duration: 0.01ms !important;
    }
}

    </style>
</head>

<body>
    <h1>CHATBOT CENIGRAF</h1>

<div class="barra-chat">
    <span class="estado-chat">Asistente virtual de Cenigraf</span>

    <button
        type="button"
        id="limpiar-chat"
        class="boton-limpiar"
    >
        Limpiar chat
    </button>
</div>

<div class="preguntas-frecuentes">
    <h2>Preguntas frecuentes</h2>

    <div class="botones-preguntas">
        <button type="button" class="pregunta-btn"
            data-pregunta="¿Qué es Cenigraf?">
            ¿Qué es Cenigraf?
        </button>

        <button type="button" class="pregunta-btn"
            data-pregunta="¿Cómo puedo conocer el centro?">
            Conoce el centro
        </button>

        <button type="button" class="pregunta-btn"
            data-pregunta="¿Qué programas presenciales ofrecen?">
            Oferta presencial
        </button>

        <button type="button" class="pregunta-btn"
            data-pregunta="¿Qué programas virtuales ofrecen?">
            Oferta virtual
        </button>

        <button type="button" class="pregunta-btn"
            data-pregunta="¿Qué es el contrato de aprendizaje?">
            Contrato de aprendizaje
        </button>

        <button type="button" class="pregunta-btn"
            data-pregunta="¿Cómo puedo consultar la oferta educativa?">
            Consultar oferta educativa
        </button>
    </div>
</div>

    <div id="chat" aria-live="polite">
        <p class="mensaje">BIENVENIDO A CHATBOT CENIGRAF</p>
         <div id="indicador-escribiendo"
         class="mensaje indicador-escribiendo"
         role="status"
         aria-live="polite"
         hidden>
        <span class="puntos-animados" aria-hidden="true"></span>
        El chatbot está escribiendo...
    </div>
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
        
const botonLimpiar = document.getElementById("limpiar-chat");
const chat = document.getElementById("chat");
const formulario = document.getElementById("formulario");
const entrada = document.getElementById("mensaje");
const botonesPreguntas = document.querySelectorAll(".pregunta-btn");
const indicador = document.getElementById("indicador-escribiendo");
const botonEnviar = formulario.querySelector("button[type='submit']");

function agregarMensaje(remitente, texto) {
    const parrafo = document.createElement("p");
    parrafo.className = "mensaje";
    parrafo.textContent = remitente + ": " + texto;

    // Insertar antes del indicador para mantenerlo al final
    chat.insertBefore(parrafo, indicador);
    chat.scrollTop = chat.scrollHeight;
}

function mostrarIndicador() {
    indicador.hidden = false;
    chat.scrollTop = chat.scrollHeight;
}

function ocultarIndicador() {
    indicador.hidden = true;
}

async function enviarPregunta(pregunta) {
    const mensaje = pregunta.trim();

    if (!mensaje || botonEnviar.disabled) {
        return;
    }

    agregarMensaje("Tú", mensaje);
    entrada.value = "";

    // Deshabilitar controles mientras se procesa la consulta
    botonEnviar.disabled = true;
    botonesPreguntas.forEach(boton => boton.disabled = true);

    // Mostrar el indicador antes de consultar la API
    mostrarIndicador();

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

        // Ocultar el indicador al recibir la respuesta
        ocultarIndicador();

        agregarMensaje("Bot", datos.reply);

    } catch (error) {
        // Ocultarlo también si se produce un error
        ocultarIndicador();

        agregarMensaje(
            "Bot",
            "No fue posible obtener una respuesta. Inténtalo de nuevo."
        );

        console.error("Error al consultar el chatbot:", error);

    } finally {
        // Garantizar que no quede visible al finalizar
        ocultarIndicador();

        botonEnviar.disabled = false;
        botonesPreguntas.forEach(boton => boton.disabled = false);
        entrada.focus();
    }
}

// Envío mediante el formulario
formulario.addEventListener("submit", async function(evento) {
    evento.preventDefault();
    await enviarPregunta(entrada.value);
});

// Envío mediante preguntas frecuentes
botonesPreguntas.forEach(boton => {
    boton.addEventListener("click", async function() {
        await enviarPregunta(boton.dataset.pregunta);
    });
});
function limpiarChat() {
    const confirmar = window.confirm(
        "¿Estás seguro de que deseas limpiar la conversación visible?"
    );

    // Si el usuario cancela, conservar la conversación
    if (!confirmar) {
        return;
    }

    // Ocultar el indicador de escritura
    ocultarIndicador();

    // Eliminar todos los mensajes del contenedor
    chat.replaceChildren();

    // Restaurar el mensaje de bienvenida
    const bienvenida = document.createElement("p");
    bienvenida.className = "mensaje";
    bienvenida.textContent = "¡Bienvenido a Chatbot Cenigraf!";
    chat.appendChild(bienvenida);

    // Permitir realizar nuevas consultas
    entrada.value = "";
    chat.scrollTop = 0;
    entrada.focus();
}

botonLimpiar.addEventListener("click", limpiarChat);

    </script>
</body>
</html>"""