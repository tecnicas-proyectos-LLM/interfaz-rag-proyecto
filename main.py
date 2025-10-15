# Importando elementos
from models.local_model import model_local_process
from models.api_model import model_api_process
from models.langchain_ollama_model import model_langchain_process
from frontend.chatbot import init_chatbot

def main():
    # Ejecutando proceso completo
    #init_chatbot( execute_model=model_local_process )
    init_chatbot( execute_model=model_langchain_process )
    # init_chatbot( execute_model=model_api_process )

if __name__ == "__main__":
    main()
