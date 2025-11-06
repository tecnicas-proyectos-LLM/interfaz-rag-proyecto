# NO SE USA POR PROBLEMAS DE CUOTA, SE REQUIERE API ASOCIADA A PROYECTO DE PAGO EN AI STUDIO

# Importando librerías

import json
from pathlib import Path
from uuid import uuid4
from .database import get_vector_resources
from langchain_core.documents import Document
import time
from typing import List

def process_batch(documents: List[Document], uuids: List[str], chroma_db, batch_size: int = 20):
"""Process documents in smaller batches"""
for i in range(0, len(documents), batch_size):
batch_docs = documents[i:i + batch_size]
batch_uuids = uuids[i:i + batch_size]

        print(f"Procesando batch {i//batch_size + 1} de {len(documents)//batch_size + 1}...")
        try:
            chroma_db.add_documents(documents=batch_docs, ids=batch_uuids)
            print(f"Batch {i//batch_size + 1} completado exitosamente")
            # Esperar 1 segundo entre batches para respetar límites de rate
            time.sleep(1.2)
        except Exception as e:
            print(f"Error en batch {i//batch_size + 1}: {str(e)}")
            # Si hay error, esperar más tiempo antes de reintentar
            time.sleep(5)
            try:
                chroma_db.add_documents(documents=batch_docs, ids=batch_uuids)
                print(f"Reintento exitoso del batch {i//batch_size + 1}")
            except Exception as e:
                print(f"Error fatal en batch {i//batch_size + 1}: {str(e)}")
                raise

def vectorize_context_chunks(): # Obteniendo configuraciones de la vector DB
settings = get_vector_resources() # Cargando los chunks del archivo JSON
print("Cargando chunks desde el archivo JSON...")
chunks_path = Path(**file**).parent.parent / 'chunks' / 'chunks_valle_de_lili.json'
with open(chunks_path, 'r', encoding='utf-8') as f:
chunks_data = json.load(f)

    print("Chunks cargados con éxito.")
    # Convertir chunks a documentos de LangChain
    print("Convirtiendo chunks a documentos de LangChain...")
    documents = []
    for chunk in chunks_data:
        doc = Document(
            page_content=chunk['content'],
            metadata=chunk['metadata']
        )
        documents.append(doc)

    print(f"Total de documentos a agregar: {len(documents)}")
    print("Creando UUIDs para los documentos...")
    uuids = [str(uuid4()) for _ in range(len(documents))]

    print("Agregando documentos a la base de datos en batches...")
    process_batch(documents, uuids, settings["chroma"], batch_size=20)
    print("Proceso completado.")

if **name** == "**main**":
vectorize_context_chunks()

# Importando librerías

import json
from pathlib import Path
from uuid import uuid4
from .database import get_vector_resources
from langchain_core.documents import Document
import time
from typing import List

def save_progress(last_processed_index: int, total_documents: int):
"""Guarda el progreso actual"""
progress_file = Path(**file**).parent / 'progress.json'
with open(progress_file, 'w') as f:
json.dump({
'last_processed_index': last_processed_index,
'total_documents': total_documents,
'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
}, f)

def load_progress():
"""Carga el último progreso guardado"""
progress_file = Path(**file**).parent / 'progress.json'
if progress_file.exists():
with open(progress_file, 'r') as f:
return json.load(f)
return {'last_processed_index': 0, 'total_documents': 0}

def process_batch(documents: List[Document], uuids: List[str], chroma_db, batch_size: int = 3, start_index: int = 0):
"""Process documents in smaller batches with progress tracking"""
total_batches = len(documents) // batch_size + (1 if len(documents) % batch_size > 0 else 0)

    for i in range(start_index, len(documents), batch_size):
        batch_docs = documents[i:i + batch_size]
        batch_uuids = uuids[i:i + batch_size]

        current_batch = i // batch_size + 1
        print(f"Procesando batch {current_batch} de {total_batches}...")

        try:
            chroma_db.add_documents(documents=batch_docs, ids=batch_uuids)
            print(f"Batch {current_batch} completado exitosamente")

            # Guardar progreso después de cada batch exitoso
            save_progress(i + batch_size, len(documents))

            time.sleep(1.2)  # Espera para respetar límites de API

        except Exception as e:
            print(f"Error en batch {current_batch}: {str(e)}")
            print("Progreso guardado hasta el batch anterior.")
            print(f"Para continuar, ejecute el script nuevamente.")
            return False

    # Eliminar archivo de progreso al completar
    progress_file = Path(__file__).parent / 'progress.json'
    if progress_file.exists():
        progress_file.unlink()
    return True

def vectorize_context_chunks(): # Cargar progreso anterior
progress = load_progress()
start_index = progress['last_processed_index']

    if start_index > 0:
        print(f"Reanudando desde el índice {start_index}...")

    # ...existing code for loading chunks and creating documents...

    # Verificar si ya hay documentos procesados
    settings = get_vector_resources()
    print("Cargando chunks desde el archivo JSON...")
    chunks_path = Path(__file__).parent.parent / 'chunks' / 'chunks_valle_de_lili.json'
    with open(chunks_path, 'r', encoding='utf-8') as f:
        chunks_data = json.load(f)

    print("Chunks cargados con éxito.")
    print("Convirtiendo chunks a documentos de LangChain...")
    documents = []
    for chunk in chunks_data:
        doc = Document(
            page_content=chunk['content'],
            metadata=chunk['metadata']
        )
        documents.append(doc)

    total_docs = len(documents)
    remaining_docs = total_docs - start_index

    print(f"Total de documentos: {total_docs}")
    print(f"Documentos restantes por procesar: {remaining_docs}")

    if remaining_docs <= 0:
        print("Todos los documentos ya han sido procesados.")
        return

    print("Creando UUIDs para los documentos restantes...")
    uuids = [str(uuid4()) for _ in range(total_docs)][start_index:]

    print("Procesando documentos restantes en batches...")
    success = process_batch(
        documents[start_index:],
        uuids,
        settings["chroma"],
        batch_size=3,
        start_index=0
    )

    if success:
        print("Proceso completado exitosamente.")
    else:
        print("Proceso interrumpido. Ejecute nuevamente para continuar.")

if **name** == "**main**":
vectorize_context_chunks()
