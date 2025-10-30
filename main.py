# Importando elementos
#from chat_models.langchain_googleAI_mode import model_langchain_google_process
from agent_models.google_model_shortMemory import agent_google_shortMemory

from frontend.chatbot import init_chatbot
#from settings.database_connection import check_connection

def main():
    # Ejecutando proceso completo
    #init_chatbot( execute_model=model_langchain_google_process )
    
    init_chatbot( execute_model=agent_google_shortMemory )

if __name__ == "__main__":
    main()
