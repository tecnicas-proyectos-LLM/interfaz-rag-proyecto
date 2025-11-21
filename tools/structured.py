# Importando paquetes
from pydantic import BaseModel, Field
from typing import Optional

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

# JSON Schema para consultar el estado de un PQRS Tool: get_pqr_status
class PqrStatusSchema( BaseModel ):
    """
        Entrada para consultar el estado de un PQRS
    """
    ticket_id: str = Field( description="ID del ticket PQRS a consultar" )

# JSON Schema para crear un PQRS Tool: create_pqr
class CreatePqrSchema( BaseModel ):
    """
        Entrada para crear un PQRS
    """
    tipo_solicitud: str = Field( description="Tipo de solicitud (Petición, Queja, Reclamo, Sugerencia)" )
    asunto: str = Field( description="Asunto del PQRS" )
    descripcion: str = Field( description="Descripción del PQRS" )
    nombre_usuario: str = Field( description="Nombre del usuario" )
    cedula: str = Field( description="Número de identificación del usuario" )
    email: str = Field( description="Correo electrónico del usuario" )
    telefono: Optional[str] = Field( default=None, description="Número de teléfono del usuario" )
    categoria: Optional[str] = Field( default="General", description="Categoría del PQRS" )

# JSON Schema para consultar resultados de laboratorio Tool: get_laboratory_results
class LaboratoryResultsSchema( BaseModel ):
    """
        Entrada para consultar resultados de laboratorio
    """
    cedula: str = Field( description="Numero de identificación del paciente" )
    orden_id: Optional[str] = Field( default=None, description="ID especifico de una orden" )
    fecha_desde: Optional[str] = Field( default=None, description="Fecha inicio búsqueda formato YYYY-MM-DD" )
    fecha_hasta: Optional[str] = Field( default=None, description="Fecha fin búsqueda formato YYYY-MM-DD" )