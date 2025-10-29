# Importando librerías
import psycopg
from settings.envs import get_envs

# Cargando variables de entorno
envs = get_envs()

def check_connection():
    """
        Esta función verifica que la conexión con la base de datos
        se establezca, y al mismo tiempo, esté activa.
    """
    try:
        with psycopg.connect( envs["postgres_url"] ) as conn:
            print("Conexión establecida y activa")
            
            return True

    except Exception as e:
        print(f"Error para establecer conexión con la base de datos: { e }")
        
        return False