# Importando paquetes
from pydantic import BaseModel, Field

# JSON Schema para solicitar citas pendientes o programadas
class PendingAppointmentsInput( BaseModel ):
    """
        Entrada para las consultas de citas
        pendientes o programadas de un paciente
    """
    cedula: str = Field( description="Número de identificación del paciente o usuario" )