# Importando librerías
import json
from langchain_core.output_parsers import StrOutputParser
from langchain.agents.middleware import dynamic_prompt, ModelRequest
from langchain.tools import tool
from vectorDB.database import get_vector_resources
from langchain_core.prompts import ChatPromptTemplate 
from agent_models.model_config import models

# Obteniendo configuraciones del vector DB
resources = get_vector_resources()

K_PER_QUERY = 5
FETCH_K = 12

EXPANSION_PROMPT = """
Eres un asistente de IA experto en sistemas de recuperación de información.
Tu tarea es tomar una consulta de usuario y generar 3 consultas de búsqueda alternativas
que sean semánticamente similares o que desglosen la pregunta original.
El objetivo es encontrar documentos relevantes en una base de datos de una clínica.


No respondas la pregunta. Solo genera las consultas.
Separa cada consulta con un salto de línea.


Consulta Original:
{query}


Consultas Alternativas:
"""


# Template para generar consultas alternativas
QUERY_EXPANSION_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", EXPANSION_PROMPT),
        ("human", "Consulta original: {query}"),
    ]
)

@dynamic_prompt
def prompt_with_context(request: ModelRequest) -> str:
    original_query = request.state["messages"][-1].text.strip()
    
    # Query expansion
    query_expansion_chain = QUERY_EXPANSION_PROMPT | models["model_RAG"] | StrOutputParser()
    alternative_queries_str = query_expansion_chain.invoke({"query": original_query})
    alternative_queries = [q.strip() for q in alternative_queries_str.split('\n') if q.strip()]
    
    all_queries = [original_query] + alternative_queries
    print(f"Consultas de búsqueda: {all_queries}")
    
    # USAR MMR en vez de similarity_search
    all_retrieved_chunks = []
    for query in all_queries:
        chunks = resources["chroma"].max_marginal_relevance_search(
            query=query,
            k=K_PER_QUERY,           # Devolver 3 por query
            fetch_k=FETCH_K,    # Buscar en 12 candidatos
            lambda_mult=0.6  # Balance relevancia/diversidad
        )
        all_retrieved_chunks.extend(chunks)
    
    print(f'Total chunks recuperados: {len(all_retrieved_chunks)}')
    
    # Eliminar duplicados
    unique_ids = set()
    unique_chunks = []
    for chunk in all_retrieved_chunks:
        chunk_id = hash(chunk.page_content)
        if chunk_id not in unique_ids:
            unique_ids.add(chunk_id)
            unique_chunks.append(chunk)
    
    print(f'Chunks únicos: {len(unique_chunks)}')

    # Filtrar chunks muy cortos DIRECTAMENTE
    MIN_CHUNK_LENGTH = 100
    filtered_chunks = [
        chunk for chunk in unique_chunks 
        if len(chunk.page_content) >= MIN_CHUNK_LENGTH
    ]
    
    print(f'Chunks después de filtrar cortos: {len(filtered_chunks)}')

    # Reordenar por longitud (priorizar medianos/largos)
    filtered_chunks.sort(key=lambda x: len(x.page_content), reverse=True)
    
    # Tomar solo los top N después de reordenar
    MAX_CHUNKS_TO_USE = 10
    final_chunks = filtered_chunks[:MAX_CHUNKS_TO_USE]

    # 7. Unir chunks
    docs_content = "\n---\n".join(doc.page_content for doc in final_chunks)

    if not docs_content:
        print("No se recuperó ningún contexto relevante.")
        return "<!-- No se encontró información relevante sobre la consulta. -->"
    
    # 8. Retornar contexto
    context_message = f"""
        Información relevante recuperada:
        {docs_content}
    """

    print(context_message)
    print(f"Contexto generado con {len(final_chunks)} chunks")
    return context_message


def generar_contacto(area: str) -> str:
    try:
        with open("tools/data/contacto.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        # El JSON tiene una lista con un diccionario
        contactos = data[0]
        print(contactos)
        return contactos.get(area.lower(), "Área no encontrada. Visita la página principal de contacto.")

    except FileNotFoundError:
        return "Archivo de contactos no encontrado."
    except Exception as e:
        return f"Error al acceder a la información de contacto: {e}"


# ----------------------------------------------------------
# TOOLS
# ----------------------------------------------------------
class ModelTools:

    # Valentina
    @tool(
        "get_contacts_to_schedule",
    description = (
        "Permite obtener información de contacto o enlaces de servicios clínicos "
        "como agendamiento de citas, urgencias o laboratorio. "
        "Usa esta herramienta cuando el usuario necesite saber cómo comunicarse "
        "con un área específica del hospital o clínica."
    )
        )
    @staticmethod
    def get_contacts_to_schedule(area: str) -> str:
        """
        Busca información de contacto de acuerdo al área solicitada.
        Args:
            area: Nombre del área (por ejemplo: 'citas', 'urgencias', 'laboratorio').
        Returns:
            Enlace o número telefónico correspondiente a la sección solicitada.
        """
        return generar_contacto(area)
    
    # Juan
    @tool
    @staticmethod
    def get_PQR() -> str:
        """Colocar descripción aquí."""
        return f"Contenido"

    # Mateo
    @tool(
        "pending_appointments", 
        description="Busca citas médicas pendientes de usuarios. Usalo cuando el usuario necesite consultar si tiene citas pendientes."
    )
    @staticmethod
    def get_pending_appointments(cedula: str) -> str:
        """
            Busca en el archivo JSON si el usuario o paciente
            tiene citas médicas pendientes o programadas.
            
            Args:
                cedula: número de identificación del usuario.
        """

        # Cargando archivo JSON donde está la información
        with open("tools/data/pending_appointments.json", "r", encoding="utf-8") as file:
            users = json.load( file )

        for user in users:
            if user["cedula"] == cedula:
                citas = user.get("citas", [])

                if len(citas) == 0:
                    return f"El usuario: { user["nombre"] }, con la cédula: { cedula } no tiene citas."

                return (
                    f"El usuario: { user["nombre"] }, con la cédula: { cedula }"
                    f"tiene las siguientes citas pendientes: { user["citas"] }"
                )                

        return "Usuario no encontrado en el sistema."
    
    # Sebastian
    @tool
    @staticmethod
    def get_vaccination_programs() -> str:
        """Colocar descripción aquí."""
        return f"Contenido"
    
    # Juan
    @tool
    @staticmethod
    def get_laboratory_results() -> str:
        """Colocar descripción aquí."""
        return f"Contenido"


