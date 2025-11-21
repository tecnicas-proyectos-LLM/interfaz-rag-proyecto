# Importando librerías
import json
import uuid
from langchain_core.output_parsers import StrOutputParser
from langchain.agents.middleware import dynamic_prompt, ModelRequest
from langchain.tools import tool
from vectorDB.database import get_vector_resources
from langchain_core.prompts import ChatPromptTemplate 
from agent_models.model_config import models
from datetime import datetime
from typing import Optional
from config.firestore_config import get_firestore_client
from tools.formatters.lab_results_formatters import format_single_lab_result, format_multiple_lab_results
from tools.structured import (
    PendingAppointmentsInput
)

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

    # print(context_message)
    print(f"Contexto generado con {len(final_chunks)} chunks")
    return context_message

# ----------------------------------------------------------
# TOOLS
# ----------------------------------------------------------

def generar_contacto(area: str) -> str:
    """
    Retorna el contacto correspondiente al área indicada,
    leyendo desde /tools/data/contacto.json.
    """
    try:
        with open("tools/data/contacto.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        contactos = data[0]

        if not isinstance(contactos, dict):
            return "El formato del archivo de contactos es inválido."

        contacto = contactos.get(area.lower())

        if contacto:
            return contacto
        else:
            return (
                f"No encontré información para el área '{area}'. "
                "Puedes visitar la página principal de contacto o preguntar por otra área."
            )

    except FileNotFoundError:
        return (
            "No pude acceder al archivo de contactos en este momento. "
            "Inténtalo nuevamente o pregunta por otra área."
        )
    except Exception as e:
        return (
            f"Ocurrió un error al procesar tu solicitud: {e}. "
            "Puedes intentar con otro servicio o volver a preguntar."
        )


class ModelTools:

    @tool(
        "get_contacts_to_schedule",
        description=(
            "Obtiene información de contacto, enlaces o canales de atención "
            "de un área específica (ej. citas, urgencias, laboratorio). "
            "Úsala cuando el usuario desee contactar un servicio clínico."
        ),
        args_schema={
            "type": "object",
            "properties": {
                "area": {
                    "type": "string",
                    "description": (
                        "Nombre del área médica o administrativa. "
                        "Ejemplos: 'laboratorio', 'citas', 'urgencias', 'imagenología'."
                    )
                }
            },
            "required": ["area"]
        }
    )
    def get_contacts_to_schedule(area: str):
        """
        Wrapper que llama a generar_contacto() y maneja errores.
        """
        try:
            return generar_contacto(area)
        except Exception:
            return (
                "Hubo un error inesperado mientras buscaba la información. "
                "Por favor, intenta nuevamente o solicita otro tipo de ayuda."
            )
    # Juan
    @tool(
        "create_pqrs",
        description="""
        Crea un ticket PQRS (Petición, Queja, Reclamo o Sugerencia) para el usuario.
        
        Usa esta herramienta cuando el usuario quiera:
        - Hacer una petición o solicitud
        - Presentar una queja
        - Registrar un reclamo
        - Dar una sugerencia
        
        IMPORTANTE: Debes obtener TODOS los parámetros requeridos del usuario
        a través de la conversación antes de llamar esta tool.
        Si falta algún parámetro, pregunta al usuario en lenguaje natural.
        """
    )
    @staticmethod
    def create_pqrs(
        tipo_solicitud: str,
        asunto: str,
        descripcion: str,
        nombre_usuario: str,
        cedula: str,
        email: str,
        telefono: Optional[str] = None,
        categoria: Optional[str] = "General"
    ) -> str:
        """
        Crea un nuevo ticket PQRS en Firestore.
        
        Args:
            tipo_solicitud: Tipo de solicitud (Petición, Queja, Reclamo, Sugerencia)
            asunto: Titulo o asunto breve del PQRS
            descripcion: Descripción detallada del problema o solicitud
            nombre_usuario: Nombre completo del usuario
            cedula: Numero de identificación del usuario
            email: Correo electrónico del usuario
            telefono: Teléfono de contacto (opcional)
            categoria: Categoría del PQRS (Medico, Administrativo, Facturación, etc.)
        
        Returns:
            Mensaje con el ID del ticket creado
        """
        
        try:
            # Generar ID único del ticket
            ticket_id = f"PQRS-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"
            
            # Preparar datos del PQRS
            pqr_data = {
                "ticket_id": ticket_id,
                "tipo_solicitud": tipo_solicitud,
                "asunto": asunto,
                "descripcion": descripcion,
                "nombre_usuario": nombre_usuario,
                "cedula": cedula,
                "email": email,
                "telefono": telefono if telefono else "No proporcionado",
                "categoria": categoria,
                "estado": "En proceso",
                "prioridad": "Media",
                "fecha_creacion": datetime.now(),
                "fecha_actualizacion": datetime.now(),
                "comentarios": [],
                "asignado_a": None
            }
            
            # Guardar en Firestore
            db = get_firestore_client()
            doc_ref = db.collection("pqrs").document(ticket_id)
            doc_ref.set(pqr_data)
            
            # Retornar respuesta exitosa
            response = (
                f"Su solicitud PQRS ha sido creada exitosamente.\n\n"
                f"Detalles del ticket:\n"
                f"- ID del Ticket: {ticket_id}\n"
                f"- Tipo: {tipo_solicitud}\n"
                f"- Asunto: {asunto}\n"
                f"- Estado: En proceso\n"
                f"- Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
                f"Recibirá una notificación por correo electrónico a {email} con el seguimiento de su solicitud.\n\n"
                f"Puede consultar el estado de su ticket en cualquier momento proporcionando el ID: {ticket_id}"
            )
            
            return response
            
        except Exception as e:
            return f"Error al crear el PQRS: {str(e)}. Por favor intente nuevamente o contacte al administrador."
    
    # Juan
    @tool(
        "get_pqr_status",
        description="Consulta el estado actual de un ticket PQRS usando su ID."
    )
    @staticmethod
    def get_pqrs_status(ticket_id: str) -> str:
        """
        Consulta el estado de un ticket PQRS en Firestore.
        
        Args:
            ticket_id: ID del ticket PQRS a consultar
            
        Returns:
            Información del estado del ticket
        """
        try:
            # Consultar en Firestore
            db = get_firestore_client()
            doc_ref = db.collection("pqrs").document(ticket_id)
            doc = doc_ref.get()
            
            if not doc.exists:
                return f"No se encontró ningún ticket con el ID: {ticket_id}"
            
            data = doc.to_dict()
            
            response = (
                f"Estado del Ticket {ticket_id}\n\n"
                f"- Tipo: {data.get('tipo_solicitud')}\n"
                f"- Asunto: {data.get('asunto')}\n"
                f"- Estado: {data.get('estado')}\n"
                f"- Prioridad: {data.get('prioridad')}\n"
                f"- Fecha de creación: {data.get('fecha_creacion').strftime('%d/%m/%Y %H:%M')}\n"
                f"- Categoría: {data.get('categoria')}\n\n"
                f"Descripción:\n{data.get('descripcion')}"
            )
            
            return response
            
        except Exception as e:
            return f"Error al consultar el ticket: {str(e)}"

    # Juan
    @tool(
        "get_laboratory_results",
        description="""
        Consulta los resultados de exámenes de laboratorio clínico del paciente.
        
        Usa esta herramienta cuando el usuario quiera:
        - Ver resultados de exámenes de laboratorio
        - Consultar analisis clinicos
        - Verificar si sus resultados están disponibles
        - Conocer valores de exámenes específicos
        
        IMPORTANTE: Necesitas la cédula del paciente para consultar.
        Si el usuario no la proporciona, pregunta amablemente.
        """
    )
    @staticmethod
    def get_laboratory_results(
        cedula: str,
        orden_id: Optional[str] = None,
        fecha_desde: Optional[str] = None,
        fecha_hasta: Optional[str] = None
    ) -> str:
        """
        Consulta resultados de laboratorio del paciente en Firestore.
        
        Args:
            cedula: Numero de identificación del paciente (obligatorio)
            orden_id: ID especifico de una orden (opcional)
            fecha_desde: Fecha inicio búsqueda formato YYYY-MM-DD (opcional)
            fecha_hasta: Fecha fin búsqueda formato YYYY-MM-DD (opcional)
        
        Returns:
            Resultados de laboratorio del paciente
        """
        
        try:
            db = get_firestore_client()
            
            # Si se proporciona orden_id especifica
            if orden_id:
                doc_ref = db.collection("laboratory_results").document(orden_id)
                doc = doc_ref.get()
                
                if not doc.exists:
                    return f"No se encontró ninguna orden con el ID: {orden_id}"
                
                data = doc.to_dict()
                
                # Verificar que la orden pertenece al paciente
                if data.get("cedula") != cedula:
                    return "El ID de orden proporcionado no corresponde a su cédula."
                
                return format_single_lab_result(data)
            
            # Buscar todas las ordenes del paciente
            query = db.collection("laboratory_results").where("cedula", "==", cedula)
            
            # Aplicar filtros de fecha si se proporcionan
            if fecha_desde:
                fecha_desde_dt = datetime.strptime(fecha_desde, "%Y-%m-%d")
                query = query.where("fecha_orden", ">=", fecha_desde_dt)
            
            if fecha_hasta:
                fecha_hasta_dt = datetime.strptime(fecha_hasta, "%Y-%m-%d")
                query = query.where("fecha_orden", "<=", fecha_hasta_dt)
            
            # Ordenar por fecha mas reciente
            query = query.order_by("fecha_orden", direction="DESCENDING").limit(10)
            
            results = query.stream()
            
            # Convertir a lista
            ordenes = [doc.to_dict() for doc in results]
            
            if not ordenes:
                return f"No se encontraron resultados de laboratorio para la cédula: {cedula}"
            
            return format_multiple_lab_results(ordenes)
            
        except Exception as e:
            return f"Error al consultar resultados de laboratorio: {str(e)}"

    # Mateo
    @tool(
        "pending_appointments",
        args_schema=PendingAppointmentsInput,
        description="""
            Busca citas médicas pendientes de usuarios. 
            Usalo cuando el usuario necesite consultar si tiene citas pendientes.
        """
    )
    @staticmethod
    def get_pending_appointments(cedula: str) -> str:
        """
            Busca en el archivo JSON si el usuario o paciente
            tiene citas médicas pendientes o programadas.
        """

        # Cargando archivo JSON donde está la información
        with open("tools/data/pending_appointments.json", "r", encoding="utf-8") as file:
            users = json.load( file )

        for user in users:
            if user["cedula"] == cedula:
                citas = user.get("citas", [])

                if len(citas) == 0:
                    return f"El usuario: { user["nombre"] }, con la cédula: { cedula }, no tiene citas."

                return f"""
                    El usuario: { user["nombre"] }, con la cédula: { cedula },
                    tiene las siguientes citas pendientes o programadas: 
                    
                    { user["citas"] }
                """          

        return "Usuario no encontrado en el sistema."
    
    # Sebastian
    @tool(
        "vaccination_programs",
        description="""
            Devuelve los esquemas de vacunación del Hospital
        """
    )
    @staticmethod
    def get_vaccination_programs() -> str:
        """
        Devuelve los esquemas de vacunación del Hospital Universitario Fundación Valle del Lili,
        obtenidos desde 'tools/data/vacunacion.json'.
        
        Contiene información de vacunas, edades y dosis recomendadas para:
        - Niños
        - Mujeres embarazadas
        - Adultos
        - Adultos mayores
        """
        import json

        try:
            with open("tools/data/vacunacion.json", "r", encoding="utf-8") as file:
                data = json.load(file)

            formatted_groups = []
            for grupo in data:
                esquema_text = "\n\n".join(
                    [
                        f"**Etapa:** {item.get('etapa', 'N/A')}\n"
                        f"**Protege de:** {', '.join(item.get('protege_de', []))}"
                        + (f"\n**Dosis:** {', '.join(item.get('dosis', []))}" if 'dosis' in item else "")
                        for item in grupo.get("esquema", [])
                    ]
                )
                formatted_groups.append(f"### {grupo['grupo']}\n{esquema_text}")

            return "\n\n".join(formatted_groups)

        except FileNotFoundError:
            return "No se encontró el archivo 'tools/data/vacunacion.json'. Verifica la ruta relativa."
        except json.JSONDecodeError:
            return "El archivo 'vacunacion.json' tiene un formato JSON inválido."
        except Exception as e:
            return f"Ocurrió un error al leer el archivo: {str(e)}"