# Importando librerías
import uuid

def generatorUUID():
    """
        Función que se encarga de generar un ID
        de manera global
    """
    id_random = uuid.uuid4()
    return id_random