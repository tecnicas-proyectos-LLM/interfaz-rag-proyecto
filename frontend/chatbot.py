# Importando framework streamlit
import streamlit as st

def chat_message(role, content):
    """
        Esta función coloca los mensajes
        en la interfaz del chatbot cada vez
        que suceda una interacción
    """
    st.chat_message( role ).markdown( content )

def settings_chatbot():
    """
        Esta función configura todos los 
        elementos necesarios para el funcionamiento de 
        la interfaz del chatbot con streamlit
    """
    st.logo("https://valledellili.org/wp-content/uploads/2025/04/LOGO_FVL_2025.svg")
    # Agregando un título al chatbot
    st.title("Chatbot Fundación Valle del Lili")

    # Creando un estado para guardar el historial
    # de las conversaciones
    if "messages" not in st.session_state:
        st.session_state["messages_chatbot"] = []

    # Proceso para mostrar todo el historial de conversaciones
    # en la interfaz del chatbot
    for message in st.session_state["messages_chatbot"]:
        role    = message["role"]
        content = message["content"]

        chat_message(role, content)

def init_chatbot( execute_model ):

    # Estableciendo configuraciones
    settings_chatbot()
    
    # Entrada del usuario
    user_input = st.chat_input("¿En qué te podemos ayudar?")

    if user_input:
        # ----------------------------------------------
        # Proceso para guardar entrada usuario en el estado
        # ----------------------------------------------
        st.session_state["messages_chatbot"].append({
            "role"   : "user",
            "content": user_input,
        })

        chat_message( role='user', content=user_input )

        # ----------------------------------------------
        # Proceso para guardar resultado modelo en el estado
        # ----------------------------------------------
        with st.spinner("Espera un momento..."):
            response = execute_model( input=user_input )

        st.session_state["messages_chatbot"].append({
            "role"   : "assistant",
            "content": response,
        })

        chat_message( role='assistant', content=response )

