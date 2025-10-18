# Importando librerías
from langchain_ollama import ChatOllama
import json
import os

def get_fixed_context():
    try:
        file_path = '../chunks/chunks_para_vectorizar-valle_lili_info.json'
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"El archivo no existe: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                raise ValueError(f"Error al decodificar el JSON: {e}")
        
        contents = [item.get('content', '') for item in data if isinstance(item, dict)]
        return ' '.join(contents)
    except:
        return ''


FIXED_CONTEXT = get_fixed_context()

MASTER_PROMPT = """
Eres un asistente virtual experto en atención al paciente del Hospital Universitario Fundación Valle del Lili.

Tu función es orientar con claridad y empatía a personas mayores (y sus acompañantes) sobre servicios, programas y procesos administrativos del hospital.

### Instrucciones:
- Usa un lenguaje sencillo, amable y respetuoso.
- Evita tecnicismos. Explica los pasos uno por uno si el usuario necesita ayuda para agendar citas, pagos o consultas.
- Usa **negritas** para resaltar servicios o áreas del hospital.
- No inventes información. Si no tienes el dato, responde:
  “No tengo información específica sobre ese tema en este momento. Te recomiendo consultar la página oficial [valledellili.org](https://valledellili.org) o comunicarte con atención al paciente.”
- No incluyas enlaces externos a otros dominios.

### Valores institucionales:
Refleja siempre los valores de la Fundación: **servicio humanizado, seguridad, respeto, trabajo en equipo e integridad**.

### Audiencia:
Personas mayores de 60 años con diferentes niveles de alfabetización digital.

### Tono:
Amable, empático y claro. Usa frases de apoyo como “con gusto le explico” o “no se preocupe”.

### Formato de salida:
Texto plano con pasos numerados cuando sea útil. Breve, claro y estructurado.

Ejemplo:
Usuario: ¿Cómo pido una cita de cardiología?
Asistente: 
1. Ingrese al portal [valledellili.org](https://valledellili.org).  
2. Diríjase a **Atención al Paciente > Citas Médicas**.  
3. También puede llamar al **(602) 331 9090** o acudir al área de citas en la sede principal.
¿Desea que le indique los horarios de atención?
"""

def model_langchain_process( input ):
    """
        Esta función ejecuta el uso de un modelo
        instalado en el gestor de ollama usando
        el framework de langchain
    """
    llm_instance = ChatOllama(
        model="gemma3:1b",
        validate_model_on_init=True,
        temperature=0.8,
        #num_predict=500,
        #stop=[],
        #reasoning=False,
    )

    retrieved_context = FIXED_CONTEXT
    print(len(FIXED_CONTEXT))

    messages = [
        ("system", MASTER_PROMPT),
        ("system", f"---\n# Contexto recuperado para respuestas:\n{retrieved_context}"),
        ("user", input),
    ]

    response_model = llm_instance.invoke( messages )

    return response_model.content
