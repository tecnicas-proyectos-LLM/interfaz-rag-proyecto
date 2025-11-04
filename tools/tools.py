# Importando librerías
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

    @staticmethod
    @tool
    def get_one(city: str) -> str:
        """Get weather for a given city."""
        return f"It's always sunny in {city}!"
    
    @staticmethod
    @tool
    def get_two(city: str) -> str:
        """Get weather for a given city."""
        return f"It's always sunny in {city}!"
    
    @staticmethod
    @tool
    def get_three(city: str) -> str:
        """Get weather for a given city."""
        return f"It's always sunny in {city}!"
    
    @staticmethod
    @tool
    def get_four(city: str) -> str:
        """Get weather for a given city."""
        return f"It's always sunny in {city}!"
    
    @staticmethod
    @tool
    def get_five(city: str) -> str:
        """Get weather for a given city."""
        return f"It's always sunny in {city}!"