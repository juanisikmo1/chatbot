"""Chatbot básico con API HTTP y una interfaz web mínima."""

from typing import Dict, List

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

app = FastAPI(title="Chatbot cenigraf", version="1.0.0")


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
    history: List[Dict[str, str]] = Field(default_factory=list)


class ChatResponse(BaseModel):
    reply: str


def responder(mensaje: str) -> str:
    """Genera una respuesta por reglas; reemplaza esta función para usar un LLM."""
    texto = mensaje.strip().lower()

    if any(saludo in texto for saludo in ("hola", "buenas", "hey")):
        return "¡Hola! ¿En qué puedo ayudarte?"
    if any(whatis in texto for whatis in (
    "que programas ofrece el sena",
    "que puedo estudiar en el sena",
    "programas disponibles",
    "carreras del sena",
    "que estudiar en el sena"
)):
        return "El SENA ofrece programas de formación técnica y tecnológica, cursos cortos, formación complementaria y cursos de idiomas, orientados al desarrollo de habilidades para el mundo laboral."

    if any(modalidad in texto for modalidad in (
    "modalidades de estudio",
    "como se estudia en el sena",
    "estudiar virtual",
    "estudiar presencial",
    "formacion virtual",
    "formacion presencial"
)):
        return "El SENA cuenta con formación presencial y virtual, dependiendo del programa. Esto permite a los aprendices elegir opciones que se adapten a sus necesidades y disponibilidad."

    if any(requisito in texto for requisito in (
    "requisitos para ingresar",
    "que necesito para estudiar",
    "requisitos del sena",
    "como puedo ingresar al sena",
    "quienes pueden estudiar"
)):
        return "Los requisitos para ingresar al SENA dependen del programa de formación. Algunos pueden exigir un nivel mínimo de escolaridad, documentos de identificación y cumplir con las condiciones establecidas en la convocatoria."

    if any(inscripcion in texto for inscripcion in (
        "como inscribirse",
        "como me inscribo",
        "inscripciones del sena",
        "inscribirme al sena",
        "proceso de inscripcion"
    )):
        return "Para inscribirte en el SENA, puedes consultar la oferta disponible en su portal oficial Betowa, seleccionar el programa que te interese y seguir las instrucciones de inscripción publicadas para esa convocatoria."

    if any(duracion in texto for duracion in (
        "cuanto dura un programa",
        "duracion de los cursos",
        "cuanto tiempo dura estudiar",
        "duracion de una carrera",
        "tiempo de formacion"
    )):
        return "La duración de los programas del SENA varía según el tipo de formación. Los cursos cortos pueden durar días o semanas, mientras que los programas técnicos y tecnológicos pueden durar varios meses o más de un año."

    if any(certificado in texto for certificado in (
        "que certificado entrega el sena",
        "certificados del sena",
        "recibir certificado",
        "certificacion del sena",
        "que titulo otorga el sena"
    )):
        return "Al finalizar y aprobar un programa de formación, el SENA puede otorgar un certificado o título según el tipo de programa cursado y los requisitos establecidos."

    if any(gratuidad in texto for gratuidad in (
        "el sena es gratis",
        "cuanto cuesta estudiar",
        "precio de los cursos",
        "estudiar gratis",
        "hay que pagar en el sena"
    )):
        return "La formación titulada y complementaria del SENA es generalmente gratuita. Consulta siempre la información oficial del programa para conocer sus condiciones y evitar posibles cobros fraudulentos."

    if any(practicas in texto for practicas in (
        "etapa productiva",
        "practicas laborales",
        "contrato de aprendizaje",
        "como se hacen las practicas",
        "experiencia laboral en el sena"
    )):
        return "Algunos programas del SENA incluyen una etapa productiva en la que el aprendiz aplica los conocimientos adquiridos en un entorno laboral. Las alternativas disponibles dependen del programa y de las normas vigentes."

    if any(beneficios in texto for beneficios in (
        "beneficios de estudiar en el sena",
        "ventajas del sena",
        "por que estudiar en el sena",
        "que ofrece el sena a los aprendices",
        "oportunidades del sena"
    )):
        return "Estudiar en el SENA permite desarrollar competencias prácticas, acceder a formación gratuita en sus programas y prepararse para oportunidades laborales o para emprender."

    if any(virtualidad in texto for virtualidad in (
        "donde encuentro los cursos",
        "pagina oficial del sena",
        "consultar oferta educativa",
        "ver programas disponibles",
        "buscar cursos del sena"
    )):
        return "Puedes consultar los programas y las convocatorias disponibles en el portal oficial del SENA: betowa.sena.edu.co. Allí podrás buscar opciones de formación y revisar sus requisitos."

    if texto.strip() == "":
        return "¡Campo vacío! Por favor, escribe una pregunta sobre la oferta educativa del SENA."

    return f"Entiendo. Cuéntame un poco más sobre: «{mensaje.strip()}»"


@app.get("/", response_class=HTMLResponse)
def pagina() -> str:
    return HTML


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    return ChatResponse(reply=responder(request.message))


HTML = r"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Chatbot Cenigraf</title>
  <style>
    body { font: 16px system-ui, sans-serif; max-width: 680px; margin: 3rem auto; padding: 0 1rem; color: #202124; }
    #chat { min-height: 260px; border: 1px solid #ddd; border-radius: 12px; padding: 1rem; margin-bottom: 1rem; }
    .message { margin: .6rem 0; white-space: pre-wrap; }
    form { display: flex; gap: .5rem; }
    input { flex: 1; padding: .8rem; border: 1px solid #aaa; border-radius: 8px; }
    button { padding: .8rem 1rem; border: 0; border-radius: 8px; background: #1459c7; color: white; cursor: pointer; }
  </style>
</head>
<body>
  <h1>Chatbot Cenigraf</h1>
  <div id="chat" aria-live="polite"><p class="message">CenigrafBot: ¡Hola! Escribe un mensaje para empezar.</p></div>
  <form id="form">
    <input id="message" autocomplete="off" placeholder="Escribe tu mensaje…" maxlength="2000">
    <button type="submit">Enviar</button>
  </form>
  <script>
    const chat = document.querySelector('#chat');
    const form = document.querySelector('#form');
    const input = document.querySelector('#message');
    function addMessage(who, text) {
      const p = document.createElement('p');
      p.className = 'message';
      p.textContent = `${who}: ${text}`;
      chat.appendChild(p);
      chat.scrollTop = chat.scrollHeight;
    }
    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      const message = input.value.trim();
      if (!message) {
  addMessage('CenigrafBot', '¡Campo vacío! Por favor, escribe un mensaje.');
  input.value = '';
  return;
}
      addMessage('Tú', message);
      input.value = '';
      try {
        const response = await fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message })
        });
        if (!response.ok) throw new Error('No se pudo obtener una respuesta.');
        const data = await response.json();
        addMessage('CenigrafBot', data.reply);
      } catch (error) {
        addMessage('CenigrafBot', `Error: ${error.message}`);
      }
    });
  </script>
</body>
</html>"""
