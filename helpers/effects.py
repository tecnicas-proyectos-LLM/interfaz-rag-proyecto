# Importando librerías
import time

def type_effect( content, message_box, delay=0.03 ):
    """
        Esta función aplica el efecto de typing
        como si el modelo respondiera poco a poco
    """
    placeholder    = message_box.empty()
    displayed_text = ""

    for char in content:
        displayed_text += char
        placeholder.markdown(displayed_text)
        time.sleep(delay)