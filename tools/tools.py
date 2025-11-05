# Importando librerías
import json

from langchain.agents.middleware import dynamic_prompt, ModelRequest
from langchain.tools import tool
from vectorDB.database import get_vector_resources

# Obteniendo configuraciones del vector DB
resources = get_vector_resources()

@dynamic_prompt
def prompt_with_context(request: ModelRequest) -> str:
    """Inject context into state messages."""
    last_query       = request.state["messages"][-1].text
    retrieved_chunks = resources["chroma"].similarity_search( last_query, k=5 )

    # Uniendo cada chunks en un bloque de texto
    docs_content = "\n\n".join( doc.page_content for doc in retrieved_chunks )

    # Regresando información relevante para complementarse en el prompt
    context_message = f"""
        Información relevante recuperada:
        { docs_content }
    """

    return context_message

# ----------------------------------------------------------
# TOOLS
# ----------------------------------------------------------
class ModelTools:

    # Valentina
    @tool
    @staticmethod
    def get_contacts_to_schedule() -> str:
        """Colocar descripción aquí."""
        return f"Contenido"
    
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