import streamlit as st

# --- CSS para el Orbe ---
css_orb = """
<style>
/* Animación de Pulso Lento (Inactivo) */
@keyframes pulse-slow {
    0% { transform: scale(1); box-shadow: 0 0 10px rgba(78, 205, 196, 0.5); }
    50% { transform: scale(1.05); box-shadow: 0 0 20px rgba(78, 205, 196, 0.8), 0 0 5px #FFFFFF; }
    100% { transform: scale(1); box-shadow: 0 0 10px rgba(78, 205, 196, 0.5); }
}

/* Animación de Pulso Rápido (Respondiendo) */
@keyframes pulse-fast {
    0% { transform: scale(1); box-shadow: 0 0 15px #6bffa6; }
    50% { transform: scale(1.1); box-shadow: 0 0 30px #BFFFBD, 0 0 15px #FFFFFF; }
    100% { transform: scale(1); box-shadow: 0 0 15px #6bffa6; }
}

@keyframes rotate-veins {
    from {
        background-position: 0% 0%; /* Posición inicial del fondo */
    }
    to {
        background-position: 100% 100%; /* Desplazamiento del fondo para simular rotación */
    }
}

/* Estilo base del Orbe */
.orb-base {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 15px;
    width: 120px;
    height: 120px;
    border-radius: 50%;
    z-index: 9999;
    /* background: linear-gradient(45deg, #A8E6CF, #5BC8AC); */
    background-image: 
        /* Capa 1: El brillo central (inspirado en orbe_2.png) */
        radial-gradient(circle at 30% 30%, #FFFFFF, transparent 35%),
        /* Capa 2: Vetas más claras (ángulos simulando remolino) */
        repeating-linear-gradient(45deg, #98d4be, #93d3bb 5%, #4aaf96 10%),
        /* Capa 3: Fondo base del orbe */
        linear-gradient(45deg, #A8E6CF, #5BC8AC);
    
    background-size: 200% 200%; /* Duplicamos el tamaño para tener espacio de movimiento */
    
    /* Ajustes visuales extra */
    border: 1px solid rgba(255, 255, 255, 0.5); /* Borde sutil */
    box-shadow: 0 0 15px rgba(168, 230, 207, 0.9);
}

/* Clase cuando el modelo está inactivo */
.orb-inactive {
    animation: pulse-slow 3s infinite ease-in-out;
}

/* Clase cuando el modelo está activo/respondiendo */
.orb-active {
    animation: pulse-fast 1s infinite alternate, 
               rotate-veins 10s linear infinite;
}
</style>
"""


def render_orb():
    """Inyecta el elemento HTML del orbe con la clase CSS correcta."""
    st.markdown(css_orb, unsafe_allow_html=True)
    
    # Determina qué clase aplicar
    is_responding = st.session_state.get('is_responding', False)
    orb_class = "orb-active" if is_responding else "orb-inactive"
    
    # Inyecta el HTML combinando la clase base y la clase dinámica
    # html_orb = f'<div class="orb-base {orb_class}"></div>'
    # st.markdown(html_orb, unsafe_allow_html=True)

    st.markdown(
        f"""
        <div style="
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
        ">
            <div class="orb-base {orb_class}"></div>
            <p>
                ¡Hola! Soy <strong>FVLia</strong>, el asistente virtual de la <strong><em>Fundación Valle del Lili</em></strong>. Te orientaré en todo
                lo que necesites sobre nuestros servicios y atención al cliente.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )