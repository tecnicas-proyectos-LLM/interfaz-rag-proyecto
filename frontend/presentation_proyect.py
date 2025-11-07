# Importando librerías
from pathlib import Path

def show_presentation( st, MASTER_PROMPT ):
    """
        Muestra la vista de presentación 
        principal con secciones de documentación del sistema.
    """
    st.markdown("# 🧭 Presentación del Proyecto")

    # -------------------------------------------------------
    # 🔹 Botón para volver al chat
    # -------------------------------------------------------
    if st.button("Volver al chat", icon="💬"):
        st.session_state["presentacion_activa"] = False
        st.rerun()
    
    st.markdown("""
    Esta presentación describe la arquitectura general del asistente FVLia,
    incluyendo el flujo de orquestación entre los componentes principales:
    el *Prompt Master*, los modelos, la base de datos vectorial, el orquestador LangChain,
    la memoria conversacional y los distintos *tools* del sistema.
    """)

    # -------------------------------------------------------
    # 🔹 FRONTEND
    # -------------------------------------------------------
    st.subheader("🎨 Frontend - Streamlit")
    with st.expander("Código de integración con streamlit"):
        ruta_archivo = Path("frontend/chatbot.py")
        if ruta_archivo.exists():
            codigo_modelo = ruta_archivo.read_text(encoding="utf-8")
            st.code(codigo_modelo.strip(), language="python")
        else:
            st.warning(f"No se encontró el archivo: {ruta_archivo}")

    # -------------------------------------------------------
    # 🔹 PROMPT MASTER
    # -------------------------------------------------------
    st.subheader("🧩 PROMPT MASTER")
    with st.expander("Descripción del Prompt Master"):
        st.markdown("""
        El *Prompt Master* define el comportamiento base del asistente: tono, rol,
        restricciones y objetivos. Actúa como el núcleo de control que contextualiza
        cada interacción antes de llamar al modelo.
        """)
        st.code(f"MASTER_PROMPT = '''{MASTER_PROMPT.strip()}'''", language="python")

    # -------------------------------------------------------
    # 🔹 CONFIGURACIÓN DE MODELOS
    # -------------------------------------------------------
    st.subheader("⚙️ Modelos Gemini")
    with st.expander("Código de la configuración de modelos"):
        ruta_archivo = Path("agent_models/model_config.py")
        if ruta_archivo.exists():
            codigo_modelo = ruta_archivo.read_text(encoding="utf-8")
            st.code(codigo_modelo.strip(), language="python")
        else:
            st.warning(f"No se encontró el archivo: {ruta_archivo}")

    # -------------------------------------------------------
    # 🔹 BASE DE DATOS VECTORIAL
    # -------------------------------------------------------
    st.subheader("🧠 Base de datos vectorial")
    with st.expander("Variables de configuración"):
        ruta_archivo = Path("vectorDB/constants.py")
        if ruta_archivo.exists():
            codigo_modelo = ruta_archivo.read_text(encoding="utf-8")
            st.code(codigo_modelo.strip(), language="python")
        else:
            st.warning(f"No se encontró el archivo: {ruta_archivo}")

    with st.expander("Configuraciones para los recursos de la vector DB"):
        ruta_archivo = Path("vectorDB/database.py")
        if ruta_archivo.exists():
            codigo_modelo = ruta_archivo.read_text(encoding="utf-8")
            st.code(codigo_modelo.strip(), language="python")
        else:
            st.warning(f"No se encontró el archivo: {ruta_archivo}")

    with st.expander("Proceso para guardar los chunks en Chroma DB"):
        ruta_archivo = Path("vectorDB/save_data.py")
        if ruta_archivo.exists():
            codigo_modelo = ruta_archivo.read_text(encoding="utf-8")
            st.code(codigo_modelo.strip(), language="python")
        else:
            st.warning(f"No se encontró el archivo: {ruta_archivo}")

    # -------------------------------------------------------
    # 🔹 LANGCHAIN ORQUESTADOR
    # -------------------------------------------------------
    st.subheader("🔄 LangChain Orquestador")
    with st.expander("Configuraciones del orquestador LangChain"):
        ruta_archivo = Path("agent_models/google_Model_shortMemory.py")
        if ruta_archivo.exists():
            codigo_modelo = ruta_archivo.read_text(encoding="utf-8")
            st.code(codigo_modelo.strip(), language="python")
        else:
            st.warning(f"No se encontró el archivo: {ruta_archivo}")

    # -------------------------------------------------------
    # 🔹 MEMORIA DEL CHAT Y CARGA DEL HISTORIAL
    # -------------------------------------------------------
    st.subheader("💬 Memoria del chat y carga del historial")
    with st.expander("Configuración de la memoria del chat y carga del historial"):
        ruta_archivo = Path("agent_models/loading.py")
        if ruta_archivo.exists():
            codigo_modelo = ruta_archivo.read_text(encoding="utf-8")
            st.code(codigo_modelo.strip(), language="python")
        else:
            st.warning(f"No se encontró el archivo: {ruta_archivo}")

    # -------------------------------------------------------
    # 🔹 TOOLS (1 a 6)
    # -------------------------------------------------------
    st.subheader("🧰 TOOLS 1–6")
    st.markdown("""
    Los *tools* amplían la capacidad del asistente, permitiéndole ejecutar acciones
    o consultar sistemas externos. Cada uno cumple una función específica.
    """)

    with st.expander("Tool 1: get_contacts_to_schedule"):
        ruta_archivo = Path("tools/tools.py")

        if ruta_archivo.exists():
            lineas = ruta_archivo.read_text(encoding="utf-8").splitlines()
            inicio, fin = 117, 153  # rango de líneas que quieres mostrar

            fragmento = "\n".join(lineas[inicio-1:fin])  # recuerda que el índice empieza en 0
            st.code(fragmento.strip(), language="python")
        else:
            st.warning(f"No se encontró el archivo: {ruta_archivo}")

        ruta_archivo = Path("tools/data/contacto.json")
        if ruta_archivo.exists():
            codigo_modelo = ruta_archivo.read_text(encoding="utf-8")
            st.code(codigo_modelo.strip(), language="json")
        else:
            st.warning(f"No se encontró el archivo: {ruta_archivo}")

        st.markdown("### Ejemplo de uso")
        st.image("frontend/imgs/tool1.png", caption="Figura 1. Arquitectura de la memoria del chat", use_container_width=True)


    with st.expander("Tool 2: get_pending_appointments"):
        ruta_archivo = Path("tools/tools.py")

        if ruta_archivo.exists():
            lineas = ruta_archivo.read_text(encoding="utf-8").splitlines()
            inicio, fin = 372, 403  # rango de líneas que quieres mostrar

            fragmento = "\n".join(lineas[inicio-1:fin])  # recuerda que el índice empieza en 0
            st.code(fragmento.strip(), language="python")
        else:
            st.warning(f"No se encontró el archivo: {ruta_archivo}")

        ruta_archivo = Path("tools/data/pending_appointments.json")
        if ruta_archivo.exists():
            codigo_modelo = ruta_archivo.read_text(encoding="utf-8")
            st.code(codigo_modelo.strip(), language="json")
        else:
            st.warning(f"No se encontró el archivo: {ruta_archivo}")

        st.markdown("### Ejemplo de uso")
        st.image("frontend/imgs/tool2.png", caption="Figura 2. Citas pendientes", use_container_width=True)


    with st.expander("Tool 3: get_vaccination_programs"):
        ruta_archivo = Path("tools/tools.py")

        if ruta_archivo.exists():
            lineas = ruta_archivo.read_text(encoding="utf-8").splitlines()
            inicio, fin = 405, 444  # rango de líneas que quieres mostrar

            fragmento = "\n".join(lineas[inicio-1:fin])  # recuerda que el índice empieza en 0
            st.code(fragmento.strip(), language="python")
        else:
            st.warning(f"No se encontró el archivo: {ruta_archivo}")

        ruta_archivo = Path("tools/data/vacunacion.json")
        if ruta_archivo.exists():
            codigo_modelo = ruta_archivo.read_text(encoding="utf-8")
            st.code(codigo_modelo.strip(), language="json")
        else:
            st.warning(f"No se encontró el archivo: {ruta_archivo}")

        st.markdown("### Ejemplo de uso")
        st.image("frontend/imgs/tool3.png", caption="Figura 3. Esquemas de vacunación", use_container_width=True)


    with st.expander("Tool 4: create_pqrs"):
        ruta_archivo = Path("tools/tools.py")

        if ruta_archivo.exists():
            lineas = ruta_archivo.read_text(encoding="utf-8").splitlines()
            inicio, fin = 155, 244  # rango de líneas que quieres mostrar

            fragmento = "\n".join(lineas[inicio-1:fin])  # recuerda que el índice empieza en 0
            st.code(fragmento.strip(), language="python")
        else:
            st.warning(f"No se encontró el archivo: {ruta_archivo}")

        st.markdown("### Ejemplo de uso")
        st.image("frontend/imgs/tool4.png", caption="Figura 4. Crear PQRS", use_container_width=True)


    with st.expander("Tool 5: get_pqr_status"):
        ruta_archivo = Path("tools/tools.py")

        if ruta_archivo.exists():
            lineas = ruta_archivo.read_text(encoding="utf-8").splitlines()
            inicio, fin = 246, 287  # rango de líneas que quieres mostrar

            fragmento = "\n".join(lineas[inicio-1:fin])  # recuerda que el índice empieza en 0
            st.code(fragmento.strip(), language="python")
        else:
            st.warning(f"No se encontró el archivo: {ruta_archivo}")

        st.markdown("### Ejemplo de uso")
        st.image("frontend/imgs/tool5.png", caption="Figura 5. Estado de PQRS", use_container_width=True)


    with st.expander("Tool 6: get_laboratory_results"):
        ruta_archivo = Path("tools/tools.py")

        if ruta_archivo.exists():
            lineas = ruta_archivo.read_text(encoding="utf-8").splitlines()
            inicio, fin = 289, 370  # rango de líneas que quieres mostrar

            fragmento = "\n".join(lineas[inicio-1:fin])  # recuerda que el índice empieza en 0
            st.code(fragmento.strip(), language="python")
        else:
            st.warning(f"No se encontró el archivo: {ruta_archivo}")

        st.markdown("### Ejemplo de uso")
        st.image("frontend/imgs/tool6_1.png", use_container_width=True)
        st.image("frontend/imgs/tool6_2.png", caption="Figura 6. Resultados de laboratorio", use_container_width=True)

    st.stop()