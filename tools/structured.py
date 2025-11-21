# Importando paquetes
from pydantic import BaseModel, Field

# JSON Schema para solicitar citas pendientes o programadas
class PendingAppointmentsInput( BaseModel ):
    """
        Entrada para las consultas de citas
        pendientes o programadas de un paciente
    """
    cedula: str = Field( description="Número de identificación del paciente o usuario" )

class GetContactsInput(BaseModel):
    """
        Entrada para busca información de
        contacto para una área
    """
    area: str = Field(
        description="Nombre del área médica o administrativa (ej. citas, urgencias, laboratorio, imagenología)."
    )
