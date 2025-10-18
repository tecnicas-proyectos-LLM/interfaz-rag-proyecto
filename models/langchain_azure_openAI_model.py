# Importando librerías
from settings.envs import get_envs
from langchain_openai import AzureChatOpenAI

from pathlib import Path
import os
import json

# Cargando variables de entorno
envs = get_envs()

def get_fixed_context():
    """
        Esta función toma los chunks y los unifica
        en una sola cadena que recibirá el modelo
        de openAI.
    """
    try:
        base_dir = Path(__file__).resolve().parent  # models/
        file_path = (base_dir.parent / 'chunks' / 'chunks_para_vectorizar-valle_lili_info.json').resolve()

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"El archivo no existe: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                raise ValueError(f"Error al decodificar el JSON: {e}")
        
        contents = [item.get('content', '') for item in data if isinstance(item, dict)]
        return ' '.join(contents)
    
    except FileNotFoundError:
        print(f"El archivo no existe: {file_path}")
        return ''
    except ValueError:
        print("Error al decodificar el JSON")
        return ''
    except:
        print('error con el contexto')
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

def langchain_azureOpenAI_model( input ):
    """
        Esta función ejecuta la lógica para
        interactuar con un modelo de OpenAI
        desde el entorno de Azure.

        Documentación: https://python.langchain.com/api_reference/openai/chat_models/langchain_openai.chat_models.azure.AzureChatOpenAI.html#langchain_openai.chat_models.azure.AzureChatOpenAI
    """
    # Configurando modelo
    llm = AzureChatOpenAI(
        azure_deployment=envs["deployment"],
        api_version=envs["version"],
        api_key=envs["api_key"],
        azure_endpoint=envs["endpoint"],
        #temperature=0,
        max_tokens=16384,
        #timeout=None,
        #max_retries=2,
        model="gpt-5-nano",
        #model_version="",
    )

    retrieved_context = FIXED_CONTEXT

    messages = [
        ("system", MASTER_PROMPT),
        ("system", f"---\n# Contexto recuperado para respuestas:\n{ retrieved_context }"),
        ("human", input),
    ]

    response_model = llm.invoke( messages )

    return response_model.content
