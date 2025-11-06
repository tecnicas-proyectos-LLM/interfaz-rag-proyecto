"""
Script para poblar Firestore con resultados de laboratorio ficticios
Ejecutar una sola vez: python scripts/populate_lab_results.py
"""

import firebase_admin
from firebase_admin import credentials, firestore
import os
from datetime import datetime, timedelta
import random
from dotenv import load_dotenv
load_dotenv()

# Inicializar Firebase (solo una vez)
def initialize_firebase():
    """Inicializa Firebase con las credenciales"""
    if not firebase_admin._apps:
        cred = credentials.Certificate({
            "type": "service_account",
            "project_id": os.getenv("FIREBASE_PROJECT_ID"),
            "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
            "private_key": os.getenv("FIREBASE_PRIVATE_KEY").replace('\\n', '\n'),
            "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
            "client_id": os.getenv("FIREBASE_CLIENT_ID"),
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_CERT_URL")
        })
        
        firebase_admin.initialize_app(cred)

def get_firestore_client():
    """Retorna el cliente de Firestore"""
    initialize_firebase()
    return firestore.client()

def generate_mock_lab_results():
    """Genera datos ficticios de resultados de laboratorio"""
    
    db = get_firestore_client()
    
    # Pacientes de prueba
    pacientes = [
        {"cedula": "969696", "nombre": "Juan David Díaz"},
        {"cedula": "747474", "nombre": "Ali Valentina Mera"},
        {"cedula": "656565", "nombre": "Mateo Olaya"},
        {"cedula": "636363", "nombre": "Sebastian Garcia"},
        {"cedula": "1234567890", "nombre": "Juan Carlos Perez Garcia"},
        {"cedula": "9876543210", "nombre": "Maria Fernanda Lopez Martinez"},
        {"cedula": "5555555555", "nombre": "Carlos Alberto Rodriguez Díaz"},
        {"cedula": "1111111111", "nombre": "Ana Sofia Gomez Ruiz"},
        {"cedula": "2222222222", "nombre": "Luis Eduardo Martinez Castro"},
    ]
    
    # Medicos
    medicos = [
        "Dra. Maria Isabel Gonzalez",
        "Dr. Roberto Carlos Jimenez",
        "Dra. Patricia Andrea Moreno",
        "Dr. Fernando Jose Ramirez",
        "Dra. Carolina Beatriz Hernandez"
    ]
    
    # Tipos de examenes
    tipos_examenes = [
        "Hematologia",
        "Quimica Clinica",
        "Inmunologia",
        "Microbiologia",
        "Coagulacion"
    ]
    
    # Definir exámenes comunes con rangos de referencia
    examenes_disponibles = {
        "Hematologia": [
            {
                "nombre_examen": "Hemoglobina",
                "codigo_loinc": "718-7",
                "unidad": "g/dL",
                "rango_min": 12.0,
                "rango_max": 16.0,
                "valor_min_mock": 10.0,
                "valor_max_mock": 18.0
            },
            {
                "nombre_examen": "Hematocrito",
                "codigo_loinc": "4544-3",
                "unidad": "%",
                "rango_min": 36.0,
                "rango_max": 48.0,
                "valor_min_mock": 30.0,
                "valor_max_mock": 52.0
            },
            {
                "nombre_examen": "Leucocitos",
                "codigo_loinc": "6690-2",
                "unidad": "x10^3/uL",
                "rango_min": 4.5,
                "rango_max": 11.0,
                "valor_min_mock": 3.0,
                "valor_max_mock": 15.0
            },
            {
                "nombre_examen": "Plaquetas",
                "codigo_loinc": "777-3",
                "unidad": "x10^3/uL",
                "rango_min": 150.0,
                "rango_max": 400.0,
                "valor_min_mock": 100.0,
                "valor_max_mock": 500.0
            }
        ],
        "Quimica Clinica": [
            {
                "nombre_examen": "Glucosa",
                "codigo_loinc": "2345-7",
                "unidad": "mg/dL",
                "rango_min": 70.0,
                "rango_max": 100.0,
                "valor_min_mock": 60.0,
                "valor_max_mock": 200.0
            },
            {
                "nombre_examen": "Creatinina",
                "codigo_loinc": "2160-0",
                "unidad": "mg/dL",
                "rango_min": 0.6,
                "rango_max": 1.2,
                "valor_min_mock": 0.4,
                "valor_max_mock": 2.0
            },
            {
                "nombre_examen": "Colesterol Total",
                "codigo_loinc": "2093-3",
                "unidad": "mg/dL",
                "rango_min": 0.0,
                "rango_max": 200.0,
                "valor_min_mock": 120.0,
                "valor_max_mock": 300.0
            },
            {
                "nombre_examen": "Trigliceridos",
                "codigo_loinc": "2571-8",
                "unidad": "mg/dL",
                "rango_min": 0.0,
                "rango_max": 150.0,
                "valor_min_mock": 80.0,
                "valor_max_mock": 250.0
            }
        ],
        "Inmunologia": [
            {
                "nombre_examen": "TSH",
                "codigo_loinc": "3016-3",
                "unidad": "uUI/mL",
                "rango_min": 0.4,
                "rango_max": 4.0,
                "valor_min_mock": 0.2,
                "valor_max_mock": 8.0
            },
            {
                "nombre_examen": "Proteina C Reactiva",
                "codigo_loinc": "1988-5",
                "unidad": "mg/L",
                "rango_min": 0.0,
                "rango_max": 5.0,
                "valor_min_mock": 0.0,
                "valor_max_mock": 20.0
            }
        ]
    }
    
    metodos = ["Espectrofotometria", "Inmunoquimioluminiscencia", "Citometria de flujo", "Enzimatico"]
    
    estados_orden = ["Disponible", "En proceso", "Pendiente"]
    
    observaciones_posibles = [
        None,
        "Muestra adecuada para el analisís",
        "Paciente en ayunas",
        "Muestra ligeramente hemolizada",
        "Se recomienda repetir en 3 meses"
    ]
    
    print("Generando resultados de laboratorio ficticios...")
    
    contador = 0
    
    # Generar 3-5 ordenes por paciente
    for paciente in pacientes:
        num_ordenes = random.randint(3, 5)
        
        for i in range(num_ordenes):
            # Generar fecha aleatoria en los últimos 6 meses
            dias_atras = random.randint(1, 180)
            fecha_orden = datetime.now() - timedelta(days=dias_atras)
            fecha_resultado = fecha_orden + timedelta(days=random.randint(1, 3))
            
            # Seleccionar tipo de examen
            tipo_examen = random.choice(tipos_examenes)
            
            # Generar ID de orden
            orden_id = f"LAB-{fecha_orden.strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
            
            # Seleccionar exámenes para este tipo
            examenes_tipo = examenes_disponibles.get(tipo_examen, [])
            
            if len(examenes_tipo) == 0:
                continue

            # Si solo hay uno, poner uno; si hay más, elige entre 2 y el máximo
            num_examenes = 1 if len(examenes_tipo) == 1 else random.randint(2, len(examenes_tipo))
            examenes_seleccionados = random.sample(examenes_tipo, num_examenes)
            
            # Generar resultados para cada examen
            examenes_resultados = []
            for examen in examenes_seleccionados:
                # Generar valor aleatorio
                valor = round(random.uniform(
                    examen['valor_min_mock'],
                    examen['valor_max_mock']
                ), 2)
                
                # Determinar estado del resultado
                if valor < examen['rango_min']:
                    estado = "Bajo"
                elif valor > examen['rango_max']:
                    # Determinar si es alto o critico (10% de probabilidad)
                    if valor > examen['rango_max'] * 1.5 and random.random() < 0.1:
                        estado = "Critico"
                    else:
                        estado = "Alto"
                else:
                    estado = "Normal"
                
                examenes_resultados.append({
                    "nombre_examen": examen['nombre_examen'],
                    "codigo_loinc": examen['codigo_loinc'],
                    "resultado_valor": str(valor),
                    "resultado_tipo": "numeric",
                    "unidad": examen['unidad'],
                    "valor_referencia_min": str(examen['rango_min']),
                    "valor_referencia_max": str(examen['rango_max']),
                    "estado_resultado": estado,
                    "metodo": random.choice(metodos),
                    "fecha_procesamiento": fecha_resultado
                })
            
            # Crear documento de orden
            orden_data = {
                "orden_id": orden_id,
                "cedula": paciente['cedula'],
                "nombre_paciente": paciente['nombre'],
                "fecha_orden": fecha_orden,
                "fecha_resultado": fecha_resultado,
                "estado": random.choice(estados_orden) if dias_atras > 5 else "Disponible",
                "tipo_examen": tipo_examen,
                "examenes": examenes_resultados,
                "medico_solicitante": random.choice(medicos),
                "observaciones": random.choice(observaciones_posibles),
                "created_at": datetime.now()
            }
            
            # Guardar en Firestore
            doc_ref = db.collection("laboratory_results").document(orden_id)
            doc_ref.set(orden_data)
            
            contador += 1
            print(f"✓ Orden {orden_id} creada para {paciente['nombre']}")
    
    print(f"\n{'='*80}")
    print(f"✓ Se crearon {contador} ordenes de laboratorio ficticias")
    print(f"✓ Datos guardados en Firestore colección: laboratory_results")
    print(f"{'='*80}\n")
    
    # Mostrar resumen de cedulas de prueba
    print("CEDULAS DE PRUEBA PARA CONSULTAR:")
    print("-" * 40)
    for paciente in pacientes:
        print(f"  - {paciente['cedula']} ({paciente['nombre']})")
    print()


if __name__ == "__main__":
    initialize_firebase()
    generate_mock_lab_results()
